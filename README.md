#  AFTA Salary Advance & Loan Calculator

An end-to-end financial tool built for employees to check advance eligibility and calculate loan repayment schedules—backed by a powerful FastAPI backend and a Streamlit frontend, containerized via Docker.

##  Architecture Overview
                    ┌──────────────────┐
                    │  Streamlit UI    │
                    │ (Frontend)       │
                    └──────┬───────────┘
                           │ HTTP
                           ▼
                 ┌────────────────────┐
                 │   FastAPI Server   │
                 │ (RESTful Backend)  │
                 └──────┬─────────────┘
                        │
                        ▼
              ┌───────────────────────┐
              │   Pandas Processing   │
              │  (Loan + Advance Calc)│
              └───────────────────────┘

## Features

-  Check salary advance eligibility by pay frequency
-  Calculate loan amortization schedules
-  visualize monthly repayment charts
-  Store and view loan history
-  Export records as downloadable CSV


##  API Endpoints (FastAPI)

###  `POST /calculate_advance`

**Request**
```json
{
  "gross_salary": 5000,
  "pay_frequency": "monthly",
  "requested_advance": 1000
}
```

**Response**
```json
{
  "eligible": true,
  "max_advance": 1500.0
}
```

---

###  `POST /calculate-loan`

**Request**
```json
{
  "name": "Alice",
  "user_id": "12345",
  "loan_amount": 10000,
  "annual_rate": 5.0,
  "term_months": 12
}
```

**Response**
```json
{
  "monthly_payment": 856.07,
  "total_repayment": 10272.81,
  "amortization_schedule": [
    {
      "Month": 1,
      "Principal": 814.40,
      "Interest": 41.67,
      "Balance": 9185.60
    },
    {
      "Month": 2,
      "Principal": 817.81,
      "Interest": 38.26,
      "Balance": 8367.79
    },
    ...
  ]
}
```

---

###  `GET /loan-records`

**Response**
```json
[
  {
    "Name": "Alice",
    "User ID": "12345",
    "Loan Amount": 10000,
    "Total Repayment": 10272.81
  },
  {
    "Name": "John",
    "User ID": "67890",
    "Loan Amount": 8000,
    "Total Repayment": 8600.50
  }
]
```

###  How Pandas is Used
- DataFrames: Used for building amortization tables row-by-row.
- Calculations: Principal/interest per month, reducing balance.
- Export: Aggregated records for CSV download using Pandas .to_csv() equivalent.
- Storage: In-memory record tracking for the session (no DB).


### Setup Guide
- Prerequisites
- Python 3.11+ (if running without Docker)
- Docker + Docker Compose (recommended)

### Project Structure
AFTA PROJECT/
├── backend/
│   ├── loan.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml

# Clone the project
git clone https://github.com/mumo-star/afta-loan-calculator.git
cd afta-loan-calculator

### Build and start containers
docker compose up --build

### Access the app
- Frontend → http://localhost:8501
- Backend API docs → http://localhost:8000/docs


### Tech Stack
Layer	                    Tool/Framework
Frontend	                Streamlit
Backend	                    FastAPI + Uvicorn
Data Logic	                Pandas
DevOps	                    Docker Compose
Versioning	                Git / GitHub