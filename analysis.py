import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Madhu@2123",
    database="redflag"
)

query = "SELECT * FROM transactions"
df = pd.read_sql(query, connection)

connection.close()

print("=" * 50)
print("       REDFLAG TRANSACTION ANALYSIS")
print("=" * 50)

print("\nTotal Transactions:", len(df))

print("\nTransaction Types:")
print(df["txn_type"].value_counts())

print("\nTransaction Status:")
print(df["status"].value_counts())

print("\nPayment Modes:")
print(df["payment_mode"].value_counts())

print("\nCities:", df["city"].nunique())

print("\nTotal Transaction Amount: ₹", round(df["amount"].sum(), 2))

print("\nAverage Transaction Amount: ₹", round(df["amount"].mean(), 2))

print("\nHighest Transaction: ₹", round(df["amount"].max(), 2))

print("\nLowest Transaction: ₹", round(df["amount"].min(), 2))

HIGH_VALUE_LIMIT = 50000

high_value = df[df["amount"] > HIGH_VALUE_LIMIT].copy()

print("\n" + "=" * 50)
print("🚩 RED FLAG 1: HIGH-VALUE TRANSACTIONS")
print("=" * 50)

print("Threshold: ₹", HIGH_VALUE_LIMIT)
print("Suspicious Transactions:", len(high_value))
print("Suspicious Amount: ₹", round(high_value["amount"].sum(), 2))

print("\nTop 10 High-Value Transactions:")
print(
    high_value[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type"]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
    .to_string(index=False)
)

failed = df[df["status"] == "FAILED"].copy()

print("\n" + "=" * 50)
print("🚩 RED FLAG 2: FAILED TRANSACTIONS")
print("=" * 50)

print("Failed Transactions:", len(failed))
print("Failed Amount: ₹", round(failed["amount"].sum(), 2))

print("\nTop 10 Failed Transactions:")
print(
    failed[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type"]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
    .to_string(index=False)
)


df["txn_time"] = pd.to_datetime(df["txn_time"])

late_night = df[
    (df["txn_time"].dt.hour >= 23) |
    (df["txn_time"].dt.hour < 5)
].copy()

print("\n" + "=" * 50)
print("🚩 RED FLAG 3: LATE-NIGHT TRANSACTIONS")
print("=" * 50)

print("Late-Night Transactions:", len(late_night))
print("Late-Night Amount: ₹", round(late_night["amount"].sum(), 2))

print("\nTop 10 Late-Night Transactions:")
print(
    late_night[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type"]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
    .to_string(index=False)
)


df = df.sort_values(["user_id", "txn_time"]).copy()

df["time_difference"] = (
    df.groupby("user_id")["txn_time"].diff().dt.total_seconds() / 60
)

rapid_transactions = df[
    (df["time_difference"] >= 0) &
    (df["time_difference"] <= 5)
].copy()

print("\n" + "=" * 50)
print("🚩 RED FLAG 4: RAPID REPEATED TRANSACTIONS")
print("=" * 50)

print("Rapid Transactions:", len(rapid_transactions))
print(
    "Rapid Transaction Amount: ₹",
    round(rapid_transactions["amount"].sum(), 2)
)

print("\nTop 10 Rapid Transactions:")
print(
    rapid_transactions[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type", "time_difference"]
    ]
    .sort_values("time_difference")
    .head(10)
    .to_string(index=False)
)


high_value_late_night = df[
    (df["amount"] > 50000) &
    (
        (df["txn_time"].dt.hour >= 23) |
        (df["txn_time"].dt.hour < 5)
    )
].copy()

print("\n" + "=" * 50)
print("🚩 RED FLAG 5: HIGH-VALUE LATE-NIGHT TRANSACTIONS")
print("=" * 50)

print("Suspicious Transactions:", len(high_value_late_night))
print(
    "Suspicious Amount: ₹",
    round(high_value_late_night["amount"].sum(), 2)
)

print("\nSuspicious Transactions:")
print(
    high_value_late_night[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type"]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
    .to_string(index=False)
)


df["risk_score"] = 0


df.loc[df["amount"] > 50000, "risk_score"] += 30

df.loc[df["status"] == "FAILED", "risk_score"] += 20
df.loc[
    (df["txn_time"].dt.hour >= 23) |
    (df["txn_time"].dt.hour < 5),
    "risk_score"
] += 20

df.loc[df["time_difference"] <= 5, "risk_score"] += 30

# Risk level
df["risk_level"] = pd.cut(
    df["risk_score"],
    bins=[-1, 29, 59, 100],
    labels=["LOW", "MEDIUM", "HIGH"]
)

print("\n" + "=" * 50)
print("🚩 OVERALL RISK ANALYSIS")
print("=" * 50)

print("\nRisk Level Distribution:")
print(df["risk_level"].value_counts())

print("\nHIGH RISK TRANSACTIONS:", 
      len(df[df["risk_level"] == "HIGH"]))

print("\nTop 10 Highest Risk Transactions:")
print(
    df[
        ["txn_id", "user_id", "amount", "txn_time",
         "payment_mode", "city", "txn_type",
         "risk_score", "risk_level"]
    ]
    .sort_values("risk_score", ascending=False)
    .head(10)
    .to_string(index=False)
)

suspicious_transactions = df[
    df["risk_level"].isin(["MEDIUM", "HIGH"])
].copy()

suspicious_transactions.to_csv(
    "suspicious_transactions.csv",
    index=False
)

print("\n" + "=" * 50)
print("✅ SUSPICIOUS TRANSACTIONS FILE CREATED")
print("=" * 50)

print("Suspicious Transactions Saved:", len(suspicious_transactions))
print("File: suspicious_transactions.csv")