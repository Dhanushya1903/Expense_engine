# Expense Reimbursement Approval Engine

## Overview

This project implements an **Explainable Expense Approval Engine** that evaluates employee expense claims and produces decisions such as:

- APPROVE
- REVIEW
- REJECT

The system uses **pure programming logic (rule-based decision tree)** and produces an explainable decision path for each claim.

The project simulates how enterprise companies automatically approve employee reimbursement requests.


## Assignment Requirements Covered

### Core Requirements

Implement hierarchy of conditions using programming logic  
No machine learning libraries used  
Decision tree style evaluation  
Output decision path  
Provide reason summary  

### Bonus Requirement

Decision rules configurable through JSON input files  
System supports input configuration via JSON instead of manual input


## Features Implemented

### Decision Outcomes
Each expense results in:

- Final decision
- Decision path
- Reason summary


### Fraud Prevention
System detects:

- Duplicate receipt submissions
- Frequent small expense claims
- Policy violations


### Employee-Level Approval Limits
Approval limits depend on employee level:

| Level  |    Description      |
|--------|---------------------|
|   L1   | Junior Employees    |
|   L2   | Mid-Level Employees |
|   L3   | Senior Employees    |

Employee levels are dynamically fetched from `employees.json`, allowing promotions without changing employee IDs.



### Supported Expense Categories

The system supports:

1. Food
2. Accommodation
3. Travel
4. Transport
5. Office Supplies
6. Training
7. Client Meeting



### Decision Storage

Expenses are stored based on outcome:

| Decision | Storage File |
|-----------|-------------|
| APPROVE | receipts.json |
| REVIEW | reviews.json |
| REJECT | rejections.json |


## Project Structure

```text
expense_engine/
│
├── main.py                # Program entry point
├── rule_engine.py         # Approval engine logic
├── employees.json         # Employee level mapping
├── rules.json             # Optional configurable rules
│
├── receipts.json          # Approved expense records
├── reviews.json           # Review expense records
├── rejections.json        # Rejected expense records
│
├── inputs/                # Sample JSON input cases
│   ├── approve.json
│   ├── review.json
│   ├── reject.json
│   └── edge_cases.json
│
├── outputs/               # Auto-generated decision outputs
│   ├── approve_output.json
│   ├── review_output.json
│   └── reject_output.json
│
├── __pycache__/           # Python compiled cache (auto-generated)
│
└── README.md              # Project documentation
```


## How the System Works

1. Expense data is loaded from JSON input.
2. Employee level is retrieved.
3. Expense validation is performed.
4. Fraud checks run.
5. Policy compliance score calculated.
6. Approval limits evaluated.
7. Decision produced.
8. Expense stored according to outcome.


## Decision Flow

Input Validation
↓
Employee Lookup
↓
Expense Category Validation
↓
Duplicate Receipt Check
↓
Fraud Detection
↓
Policy Compliance Calculation
↓
Monthly Limit Evaluation
↓
Category Limit Evaluation
↓
Decision Output
↓
Decision Storage



## Running the Program

### Requirements
- Python 3.x installed

### Run Using Input File



python main.py inputs/approve.json


or



python main.py inputs/reject_no_receipt.json


No manual input required.


## Input Configuration Format

Example:

```json
{
  "expense": {
    "employee_id": "1001",
    "expense_type": "food",
    "expense_amount": 1200,
    "monthly_expense_total": 8000,
    "receipt_uploaded": true,
    "receipt_id": "R5001"
  }
}
```


## Edge Cases Handled

The engine handles:

- Invalid employee IDs
- Negative expense values
- Missing receipts
- Duplicate receipts
- Invalid expense categories
- Monthly limit violations
- Fraud patterns
- Empty or incorrect inputs

### Scalability Considerations

In real enterprise systems:

- Employee data typically comes from HR databases
- Storage uses relational or NoSQL databases
- Approval engines connect via APIs

## Conclusion

This project demonstrates an explainable, rule-based approval system suitable for enterprise expense automation.

The system is scalable, configurable, and demonstrates real-world decision automation principles.