# PayPilot AI 💳

**AI-powered payment recovery and customer growth agent**

PayPilot AI is a prototype for the **AI Growth & Agentic Commerce** track. It analyzes a payment situation and recommends the next best action to reduce payment drop-offs and improve customer conversion.

## Problem

Online businesses lose revenue when payments fail because of bank declines, timeouts, insufficient funds, or repeated attempts. Manual recovery can be slow and can also annoy customers with unnecessary retries.

## Solution

PayPilot AI uses a decision engine to:

- estimate payment recovery probability
- prioritize recoverable transactions
- recommend a smart retry, alternate payment method, or personalized recovery message
- generate a customer-friendly recovery message
- avoid aggressive retries after repeated failures

## Demo

The prototype runs in Streamlit and uses simulated transaction inputs. No real payment credentials are required.

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

```text
Transaction Input
       ↓
PayPilot Decision Engine
       ↓
Risk + Customer Context
       ↓
Next Best Action
   ↙      ↓       ↘
Retry   Alternate  Message
       Payment
```

## Future scope

- Razorpay test-mode integration
- real-time payment webhooks
- transaction-level ML model
- LLM-based personalized communication
- merchant analytics dashboard
- A/B testing of recovery strategies
- privacy, audit logs, and human approval controls

## Disclaimer

This is an internship prototype using simulated data. It does not process real payments and should not be used for production financial decisions without appropriate validation, security, compliance, and human oversight.
