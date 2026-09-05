def recommend_action(amount, payment_method, attempts, customer_value, failure_reason):
    score = 70
    reasons = []

    if failure_reason == "Successful":
        return {
            "recovery_probability": 100,
            "priority": "Low",
            "action": "Upsell / retention",
            "reasons": ["Payment completed successfully.", "Customer can be considered for retention or cross-sell actions."],
            "impact": "Protects successful conversions and creates an opportunity for repeat purchases.",
            "message": "Thanks for your payment! We hope you enjoyed your purchase. We'd love to help with your next order."
        }

    if failure_reason == "Pending":
        score += 5
        reasons.append("Payment is pending, so an immediate duplicate charge should be avoided.")
        action = "Monitor + notify"
    else:
        if failure_reason == "Failed - timeout":
            score += 10
            reasons.append("Timeout failures can often succeed on a controlled retry.")
        elif failure_reason == "Failed - bank decline":
            score -= 10
            reasons.append("Bank declines need a safer alternate-payment suggestion.")
        elif failure_reason == "Failed - insufficient funds":
            score -= 15
            reasons.append("Insufficient funds reduce the value of an immediate retry.")

        if attempts == 0:
            score += 10
            reasons.append("No previous retry has been attempted.")
        elif attempts >= 3:
            score -= 20
            reasons.append("Multiple attempts increase the risk of customer frustration.")

        if customer_value == "High-value":
            score += 10
            reasons.append("High-value customers receive higher recovery priority.")
        elif customer_value == "New":
            score -= 3
            reasons.append("New customers benefit from low-friction recovery messaging.")

        if payment_method == "UPI":
            reasons.append("UPI can be offered again when the failure is temporary.")
        else:
            reasons.append("An alternate payment method can reduce repeated failures.")

        if score >= 75:
            action = "Smart retry"
        elif score >= 55:
            action = "Offer alternate payment"
        else:
            action = "Personalized recovery message"

    score = max(5, min(95, score))

    if score >= 75:
        priority = "High"
        impact = "Prioritizes likely recoverable payments while minimizing unnecessary customer friction."
    elif score >= 55:
        priority = "Medium"
        impact = "Balances recovery potential with customer experience and retry fatigue."
    else:
        priority = "Low"
        impact = "Avoids aggressive retries and focuses on a helpful recovery path."

    message = (
        f"Hi! We couldn't complete your ₹{amount:,.0f} payment. "
        "You can safely try again or choose another payment method. "
        "If the issue continues, please contact support."
    )

    return {
        "recovery_probability": score,
        "priority": priority,
        "action": action,
        "reasons": reasons,
        "impact": impact,
        "message": message,
    }
