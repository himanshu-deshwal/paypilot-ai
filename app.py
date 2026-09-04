import streamlit as st
import pandas as pd
from decision_engine import recommend_action

st.set_page_config(page_title="PayPilot AI", page_icon="💳", layout="wide")

st.title("💳 PayPilot AI")
st.caption("AI-powered payment recovery and customer growth agent")

st.info("Demo mode: transaction data is simulated. No real customer or payment credentials are used.")

with st.sidebar:
    st.header("Transaction")
    amount = st.number_input("Amount (₹)", min_value=1.0, value=1499.0, step=100.0)
    payment_method = st.selectbox("Payment method", ["UPI", "Card", "Net Banking", "Wallet"])
    attempts = st.slider("Previous payment attempts", 0, 5, 1)
    customer_value = st.selectbox("Customer value", ["New", "Regular", "High-value"])
    failure_reason = st.selectbox(
        "Latest payment status",
        ["Failed - bank decline", "Failed - timeout", "Failed - insufficient funds",
         "Pending", "Successful"]
    )

if st.button("Run PayPilot Agent", type="primary"):
    result = recommend_action(
        amount=amount,
        payment_method=payment_method,
        attempts=attempts,
        customer_value=customer_value,
        failure_reason=failure_reason,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Recovery probability", f"{result['recovery_probability']}%")
    c2.metric("Priority", result["priority"])
    c3.metric("Recommended action", result["action"])

    st.subheader("🤖 Agent reasoning")
    for reason in result["reasons"]:
        st.write("•", reason)

    st.subheader("📈 Expected business impact")
    st.write(result["impact"])

    st.subheader("💬 Suggested customer message")
    st.code(result["message"], language="text")

    st.caption("This prototype demonstrates the decision workflow; production deployment should use verified payment-provider APIs, privacy controls, monitoring, and human oversight.")
