import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RedFlag Transactions",
    page_icon="🚩",
    layout="wide"
)


st.title("🚩 RedFlag Transactions")
st.subheader("Financial Fraud & Suspicious Transaction Detection")


df = pd.read_csv("suspicious_transactions.csv")

# Convert transaction time
df["txn_time"] = pd.to_datetime(df["txn_time"])


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Suspicious Transactions",
    len(df)
)

col2.metric(
    "High Risk",
    len(df[df["risk_level"] == "HIGH"])
)

col3.metric(
    "Medium Risk",
    len(df[df["risk_level"] == "MEDIUM"])
)

col4.metric(
    "Suspicious Amount",
    f"₹{df['amount'].sum():,.2f}"
)

st.divider()


st.subheader("📊 Risk Level Distribution")

risk_counts = df["risk_level"].value_counts()

st.bar_chart(risk_counts)

st.subheader("💳 Suspicious Transactions by Payment Mode")

payment_counts = df["payment_mode"].value_counts()

st.bar_chart(payment_counts)

st.subheader("🏙️ Suspicious Transactions by City")

city_counts = df["city"].value_counts()

st.bar_chart(city_counts)

st.subheader("🔎 Filter Suspicious Transactions")

selected_risk = st.multiselect(
    "Select Risk Level",
    options=["HIGH", "MEDIUM"],
    default=["HIGH", "MEDIUM"]
)

filtered_df = df[
    df["risk_level"].isin(selected_risk)
]

st.write(
    "Showing",
    len(filtered_df),
    "suspicious transactions"
)

st.subheader("🚩 Suspicious Transaction Details")

st.dataframe(
    filtered_df[
        [
            "txn_id",
            "user_id",
            "amount",
            "txn_time",
            "payment_mode",
            "city",
            "txn_type",
            "risk_score",
            "risk_level"
        ]
    ].sort_values(
        "risk_score",
        ascending=False
    ),
    use_container_width=True
)