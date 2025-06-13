from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from typing import List
import pandas as pd
import uuid

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums and Schemas
class PayFrequency(str, Enum):
    monthly = "monthly"
    weekly = "weekly"

class AdvanceRequest(BaseModel):
    gross_salary: float
    requested_advance: float
    pay_frequency: PayFrequency

class AdvanceResponse(BaseModel):
    eligible: bool
    max_advance: float

class LoanRequest(BaseModel):
    name: str
    user_id: str
    loan_amount: float
    annual_rate: float
    term_months: int

class LoanResponse(BaseModel):
    loan_id: str
    monthly_payment: float
    total_repayment: float
    amortization_schedule: List[dict]

# Initialize a DataFrame to store loan records
loan_records_df = pd.DataFrame(columns=[
    "loan_id", "name", "user_id", "loan_amount",
    "annual_rate", "term_months", "monthly_payment", "total_repayment"
])

# Route: Root
@app.get("/")
def root():
    return {"message": "Welcome to the Loan Calculator API"}

# Route: Calculate Advance
@app.post("/calculate_advance", response_model=AdvanceResponse)
def calculate_advance(request: AdvanceRequest):
    if request.gross_salary <= 0 or request.requested_advance <= 0:
        raise HTTPException(status_code=400, detail="Values must be positive.")

    monthly_salary = (
        request.gross_salary * 52 / 12 if request.pay_frequency == PayFrequency.weekly
        else request.gross_salary
    )
    max_advance = monthly_salary * 0.5
    eligible = request.requested_advance <= max_advance

    return AdvanceResponse(eligible=eligible, max_advance=max_advance)

# Route: Calculate Loan and Save to DataFrame
@app.post("/calculate_loan", response_model=LoanResponse)
def calculate_loan(request: LoanRequest):
    global loan_records_df

    if request.loan_amount <= 0 or request.annual_rate < 0 or request.term_months <= 0:
        raise HTTPException(status_code=400, detail="Invalid loan input.")

    monthly_rate = request.annual_rate / 100 / 12
    loan_id = str(uuid.uuid4())[:8]

    if monthly_rate == 0:
        monthly_payment = request.loan_amount / request.term_months
    else:
        monthly_payment = (
            request.loan_amount * monthly_rate
        ) / (1 - (1 + monthly_rate) ** -request.term_months)

    total_repayment = monthly_payment * request.term_months

    # Amortization schedule
    balance = request.loan_amount
    amortization = []
    for i in range(1, request.term_months + 1):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        amortization.append({
            "Month": i,
            "Principal": round(principal, 2),
            "Interest": round(interest, 2),
            "Balance": round(balance if balance > 0 else 0, 2)
        })

    # Append to DataFrame
    new_record = {
        "loan_id": loan_id,
        "name": request.name,
        "user_id": request.user_id,
        "loan_amount": request.loan_amount,
        "annual_rate": request.annual_rate,
        "term_months": request.term_months,
        "monthly_payment": round(monthly_payment, 2),
        "total_repayment": round(total_repayment, 2)
    }
    loan_records_df = pd.concat([loan_records_df, pd.DataFrame([new_record])], ignore_index=True)

    return LoanResponse(
        loan_id=loan_id,
        monthly_payment=round(monthly_payment, 2),
        total_repayment=round(total_repayment, 2),
        amortization_schedule=amortization
    )

# Route: Get All Loan Records (for frontend display/download)
@app.get("/loan_records")
def get_all_loan_records():
    global loan_records_df
    return loan_records_df.to_dict(orient="records")
