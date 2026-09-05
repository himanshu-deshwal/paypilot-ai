import streamlit as st
import pandas as pd
from decision_engine import recommend_action

st.set_page_config(
    page_title="PayPilot AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {font-size: 2.4rem; font-weight: 750; margin-bottom: .1rem;}
    .subtitle {font-size: 1.05rem; opacity: .72; margin-bottom: 1.2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">💳 PayPilot AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Payment recovery & customer growth decision agent</div>',
    unsafe_allow_html=True,
)

st.info(
    "🧪 Demo mode — transaction data is simulated. "
    "No real customer data, payment credentials, or live payment actions are used."
)

with st.sidebar:
    st.header("⚙️ Transaction context")

    amount = st.number_input(
        "Payment amount (₹)", min_value=1.0, value=1499.0, step=100.0
    )

    payment_method = st.selectbox(
        "Payment method", ["UPI", "Card", "Net Banking", "Wallet"]
    )

    attempts = st.slider(
        "Previous payment attempts",
        0, 5, 1,
        help="Higher retry counts can increase customer friction.",
    )

    customer_value = st.selectbox(
        "Customer value", ["New", "Regular", "High-value"]
    )

    failure_reason = st.selectbox(
        "Latest payment status",
        [
            "Failed - bank decline",
            "Failed - timeout",
            "Failed - insufficient funds",
            "Pending",
            "Successful",
        ],
    )

    run_agent = st.button(
        "🚀 Run PayPilot Agent",
        type="primary",
        use_container_width=True,
    )

if not run_agent:
    st.subheader("What PayPilot does")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔎 Analyze")
        st.write(
            "Evaluates payment status, retry history, payment method, "
            "amount, and customer value."
        )

    with col2:
        st.markdown("### 🧠 Decide")
        st.write(
            "Estimates recovery potential and selects a next-best recovery action."
        )

    with col3:
        st.markdown("### 💬 Recover")
        st.write(
            "Creates a customer-friendly message while avoiding unnecessary retry pressure."
        )

    st.divider()
    st.caption(
        "Transaction Context → Decision Engine → Recovery Recommendation → "
        "Customer Communication"
    )

else:
    result = recommend_action(
        amount=amount,
        payment_method=payment_method,
        attempts=attempts,
        customer_value=customer_value,
        failure_reason=failure_reason,
    )

    st.subheader("🎯 PayPilot recommendation")

    c1, c2, c3 = st.columns(3)
    c1.metric("Recovery probability", f"{result['recovery_probability']}%")
    c2.metric("Priority", result["priority"])
    c3.metric("Next-best action", result["action"])

    st.divider()

    left, right = st.columns([1, 1])

    with left:
        st.subheader("🤖 Agent reasoning")
        for reason in result["reasons"]:
            st.write("•", reason)

        st.subheader("📈 Expected business impact")
        st.write(result["impact"])

    with right:
        st.subheader("💬 Suggested customer message")
        st.code(result["message"], language="text")

        st.subheader("📋 Transaction summary")
        summary = pd.DataFrame(
            {
                "Field": [
                    "Amount",
                    "Payment method",
                    "Previous attempts",
                    "Customer value",
                    "Latest status",
                ],
                "Value": [
                    f"₹{amount:,.0f}",
                    payment_method,
                    str(attempts),
                    customer_value,
                    failure_reason,
                ],
            }
        )
        st.dataframe(summary, hide_index=True, use_container_width=True)

    st.divider()
    st.caption(
        "Prototype only. Production deployment should use verified payment-provider APIs, "
        "privacy controls, monitoring, audit logs, and appropriate human oversight."
    )
