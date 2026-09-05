def recommend_action(amount, payment_method, attempts, customer_value, failure_reason):
    """
    PayPilot AI decision engine.

    This prototype uses transparent rule-based scoring to estimate
    payment recovery potential and recommend the next-best action.
    """

    score = 70
    reasons = []

    # -----------------------------
    # 1. Handle successful payments
    # -----------------------------
    if failure_reason == "Successful":
        return {
            "recovery_probability": 100,
            "priority": "Low",
            "action": "Upsell / retention",
            "reasons": [
                "Payment completed successfully.",
                "Recovery is unnecessary, so the focus shifts to retention."
            ],
            "impact": (
                "Protects successful conversions and creates an opportunity "
                "for repeat purchases or cross-sell."
            ),
            "message": (
                "Thanks for your payment! We hope you enjoyed your purchase. "
                "We'd love to help with your next order."
            ),
        }

    # -----------------------------
    # 2. Pending payment
    # -----------------------------
    if failure_reason == "Pending":
        return {
            "recovery_probability": 75,
            "priority": "Medium",
            "action": "Monitor + notify",
            "reasons": [
                "Payment is still pending.",
                "An immediate duplicate charge should be avoided."
            ],
            "impact": (
                "Reduces duplicate-payment risk while keeping the customer "
                "informed about the transaction status."
            ),
            "message": (
                f"Hi! Your ₹{amount:,.0f} payment is still being processed. "
                "Please wait a moment before trying again. We'll update you "
                "once the payment status is confirmed."
            ),
        }

    # -----------------------------
    # 3. Failure reason
    # -----------------------------
    if failure_reason == "Failed - timeout":
        score += 12
        reasons.append(
            "The payment timed out, so a controlled retry may recover it."
        )

    elif failure_reason == "Failed - bank decline":
        score -= 12
        reasons.append(
            "The bank declined the payment, so an alternate payment method "
            "is safer than repeated retries."
        )

    elif failure_reason == "Failed - insufficient funds":
        score -= 18
        reasons.append(
            "Insufficient funds make an immediate retry less likely to succeed."
        )

    # -----------------------------
    # 4. Retry fatigue
    # -----------------------------
    if attempts == 0:
        score += 10
        reasons.append(
            "No previous retry has been attempted, so recovery friction is low."
        )

    elif attempts == 1:
        score += 4
        reasons.append(
            "Only one previous attempt exists, allowing a limited recovery attempt."
        )

    elif attempts == 2:
        score -= 8
        reasons.append(
            "Two previous attempts suggest increasing retry fatigue."
        )

    elif attempts >= 3:
        score -= 22
        reasons.append(
            "Multiple failed attempts increase customer frustration risk."
        )

    # -----------------------------
    # 5. Customer value
    # -----------------------------
    if customer_value == "High-value":
        score += 10
        reasons.append(
            "High-value customers receive higher recovery priority."
        )

    elif customer_value == "New":
        score -= 3
        reasons.append(
            "New customers should receive a low-friction recovery experience."
        )

    else:
        reasons.append(
            "Regular customers receive a balanced recovery approach."
        )

    # -----------------------------
    # 6. Payment method
    # -----------------------------
    if payment_method == "UPI":
        reasons.append(
            "UPI can be offered again when the failure appears temporary."
        )

    elif payment_method == "Card":
        reasons.append(
            "An alternate payment method can reduce repeated card failures."
        )

    elif payment_method == "Net Banking":
        reasons.append(
            "A different payment method can provide a smoother recovery path."
        )

    else:
        reasons.append(
            "An alternate payment option can reduce repeated payment friction."
        )

    # -----------------------------
    # 7. Amount sensitivity
    # -----------------------------
    if amount >= 5000:
        score += 5
        reasons.append(
            "Higher-value transactions justify additional recovery attention."
        )

    elif amount <= 500:
        score -= 2
        reasons.append(
            "Lower-value transactions favor a lightweight recovery experience."
        )

    # -----------------------------
    # 8. Keep score realistic
    # -----------------------------
    score = max(5, min(95, score))

    # -----------------------------
    # 9. Next-best action
    # -----------------------------
    if score >= 80:
        action = "Smart retry"
        priority = "High"
        impact = (
            "Prioritizes highly recoverable payments while keeping retries "
            "controlled and customer-friendly."
        )

    elif score >= 60:
        action = "Offer alternate payment"
        priority = "Medium"
        impact = (
            "Balances recovery potential with customer experience and "
            "reduces unnecessary repeated attempts."
        )

    else:
        action = "Personalized recovery message"
        priority = "Low"
        impact = (
            "Avoids aggressive retries and focuses on a helpful recovery "
            "path for lower-probability transactions."
        )

    # -----------------------------
    # 10. Personalized message
    # -----------------------------
    if failure_reason == "Failed - timeout":
        message = (
            f"Hi! We couldn't complete your ₹{amount:,.0f} payment because "
            "the payment request timed out. You can try again once, or choose "
            "another payment method if the issue continues."
        )

    elif failure_reason == "Failed - bank decline":
        message = (
            f"Hi! Your ₹{amount:,.0f} payment was declined by the bank. "
            "Please try another payment method to complete your purchase."
        )

    elif failure_reason == "Failed - insufficient funds":
        message = (
            f"Hi! We couldn't complete your ₹{amount:,.0f} payment because "
            "the available balance may be insufficient. Please check your "
            "balance or choose another payment method."
        )

    else:
        message = (
            f"Hi! We couldn't complete your ₹{amount:,.0f} payment. "
            "You can try another payment method or contact support if the "
            "issue continues."
        )

    return {
        "recovery_probability": score,
        "priority": priority,
        "action": action,
        "reasons": reasons,
        "impact": impact,
        "message": message,
    }

