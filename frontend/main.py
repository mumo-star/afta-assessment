import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Salary Advance and Loan Calculator", layout="wide")
st.title("Salary Advance and Loan Calculator")

st.markdown("""
Welcome to the Advanced Salary and Loan Management Tool.  
This application helps you:

- Check your eligibility for a salary advance.
- Calculate detailed loan payments based on your input.
- View a line chart showing your loan repayment breakdown over time.
- Download your loan records for reference.

The tool is user-friendly and designed for employees to make informed financial decisions quickly and securely.
""")

st.subheader("User Information")

st.markdown("Enter your name.")
name = st.text_input("Name", placeholder="Enter your name")

st.markdown("Enter your ID")
user_id = st.text_input("User ID", placeholder="Enter your ID")

if not name or not user_id:
    st.warning("Please enter your name and ID to continue.")

st.markdown("---")

col1, col2 = st.columns(2)

# Replace local backend with deployed backend URL
API_BASE = "https://afta-assessment-6.onrender.com"

with col1:
    st.header("Salary Advance")
    
    st.markdown("Step 1:Enter your gross salary($):Total salary before deductions")
    gross_salary = st.number_input("Gross Salary", min_value=0.0)
    
    st.markdown("Step 2:Choose your pay frequency:How often you receive your salary")
    pay_frequency = st.selectbox("Pay Frequency", ["Monthly", "Weekly"])
    
    st.markdown("Step 3:Enter the advance amount you want in ($)")
    requested_advance = st.number_input("Requested Advance", min_value=0.0)

    st.markdown("Step 4:Check your advance eligibility")
    if st.button("Check Advance Eligibility"):
        if gross_salary <= 0 or requested_advance <= 0:
            st.warning("Please fill in gross salary and advance correctly.")
        else:
            try:
                res = requests.post(f"{API_BASE}/calculate_advance", json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency.lower(),
                    "requested_advance": requested_advance
                })
                res.raise_for_status()
                result = res.json()
                st.success(f"Eligible: {result['eligible']}")
                st.info(f"Maximum Advance: ${result['max_advance']:,.2f}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

with col2:
    st.header("Loan Calculator")
    
    st.markdown("Step 1:Enter the loan amount you want in ($) ")
    loan_amount = st.number_input("Loan Amount", min_value=0.0, max_value=100000.0)
    
    st.markdown("Step 2:Enter the annual interest rate in percentage")
    annual_rate = st.number_input("Interest Rate (%)", min_value=0.0)
    
    st.markdown("Step 3:Enter the loan term in months")
    term_months = st.number_input("Loan Term (months)", min_value=1, step=1)

    if st.button("Calculate Loan"):
        if loan_amount <= 0 or annual_rate < 0 or term_months <= 0:
            st.warning("Please enter valid loan details.")
        else:
            try:
                res = requests.post(f"{API_BASE}/calculate_loan", json={
                    "name": name,
                    "user_id": user_id,
                    "loan_amount": loan_amount,
                    "annual_rate": annual_rate,
                    "term_months": int(term_months)
                })
                res.raise_for_status()
                result = res.json()

                st.success(f"Monthly Payment: ${result['monthly_payment']:,.2f}")
                st.info(f"Total Repayment: ${result['total_repayment']:,.2f}")

                # Line Chart (if amortization data returned)
                schedule = result.get("amortization_schedule", [])
                if schedule:
                    months = [row["Month"] for row in schedule]
                    principals = [row["Principal"] for row in schedule]
                    interests = [row["Interest"] for row in schedule]
                    balances = [row["Balance"] for row in schedule]

                    st.subheader("Loan Amortization Line Chart")
                    fig, ax = plt.subplots()
                    ax.plot(months, principals, label="Principal", color="green", marker="o")
                    ax.plot(months, interests, label="Interest", color="red", marker="x")
                    ax.plot(months, balances, label="Balance", color="blue", linestyle="--")
                    ax.set_xlabel("Month")
                    ax.set_ylabel("Amount ($)")
                    ax.set_title("Loan Amortization Over Time")
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)

            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")


# Display and Download Loan Records
st.markdown("---")
st.header("All Saved Loan Records")

try:
    res = requests.get(f"{API_BASE}/loan_records")
    res.raise_for_status()
    records = res.json()

    if records:
        st.write("Loan Records:")
        st.table(records)

        # Convert to CSV format string for download
        header = records[0].keys()
        csv_string = ",".join(header) + "\n"
        for row in records:
            csv_string += ",".join(str(row[key]) for key in header) + "\n"

        st.download_button(
            label="Download Loan Records",
            data=csv_string,
            file_name="loan_records.csv",
            mime="text/csv"
        )
    else:
        st.info("No loan records found.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching loan records: {e}")
