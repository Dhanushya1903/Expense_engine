import json
import os


class ApprovalEngine:

    RECEIPT_FILE = "receipts.json"

    # Employee-level limits
    LEVEL_LIMITS = {
        "L1": {"food": 1500, "hotel": 6000, "travel": 8000},
        "L2": {"food": 2000, "hotel": 8000, "travel": 10000},
        "L3": {"food": 3000, "hotel": 12000, "travel": 15000}
    }

    MONTHLY_LIMIT = 50000

    # Storage Handling
    def load_data(self):
        if not os.path.exists(self.RECEIPT_FILE):
            return {"used_receipts": [], "expense_history": []}

        with open(self.RECEIPT_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.RECEIPT_FILE, "w") as f:
            json.dump(data, f, indent=2)

    # Employee Level Detection
    def get_employee_level(self, employee_id):

        if not employee_id.startswith("E"):
            return None

        try:
            num = int(employee_id[1:])
        except ValueError:
            return None

        if 101 <= num <= 200:
            return "L1"
        elif 201 <= num <= 300:
            return "L2"
        elif 301 <= num <= 400:
            return "L3"
        else:
            return None

    # Duplicate Receipt Detection
    def is_duplicate_receipt(self, receipt_id):
        data = self.load_data()
        return receipt_id in data["used_receipts"]

    def store_receipt(self, receipt_id, expense):
        data = self.load_data()
        data["used_receipts"].append(receipt_id)
        data["expense_history"].append(expense)
        self.save_data(data)

    # Fraud Detection
    def frequent_small_claims(self, employee_id):
        data = self.load_data()

        small_claims = [
            e for e in data["expense_history"]
            if e["employee_id"] == employee_id
            and e["expense_amount"] < 2000
        ]

        return len(small_claims) >= 5

    # Policy Compliance Score
    def calculate_policy_score(self, expense):

        total_rules = 4
        passed = 0

        level = expense["employee_level"]
        category = expense["expense_type"].lower()

        if expense["receipt_uploaded"]:
            passed += 1

        if level in self.LEVEL_LIMITS and category in self.LEVEL_LIMITS[level]:
            passed += 1

        limit = self.LEVEL_LIMITS.get(level, {}).get(category, 0)

        if expense["expense_amount"] <= limit:
            passed += 1

        if expense["monthly_expense_total"] <= self.MONTHLY_LIMIT:
            passed += 1

        return (passed / total_rules) * 100

    # Decision Tree Evaluation
    def evaluate(self, expense):

        decision_path = []
        reasons = []

        employee_id = expense["employee_id"]

        # Employee validation
        level = self.get_employee_level(employee_id)

        if level is None:
            return "REJECT", ["Invalid employee ID"], ["Employee ID invalid or outside company range."]

        expense["employee_level"] = level
        category = expense["expense_type"].lower()

        decision_path.append(f"Employee level detected as {level}")

        # Input validation
        if expense["expense_amount"] <= 0:
            return "REJECT", ["Invalid expense amount"], ["Expense must be positive."]

        if category not in self.LEVEL_LIMITS[level]:
            return "REJECT", ["Invalid expense type"], ["Unsupported expense category."]

        # Duplicate receipt 
        if self.is_duplicate_receipt(expense["receipt_id"]):
            decision_path.append("Duplicate receipt detected → REJECT")
            reasons.append("Receipt already used previously.")
            return "REJECT", decision_path, reasons

        decision_path.append("Receipt ID unique → Continue")

        # Fraud detection 
        if self.frequent_small_claims(employee_id):
            decision_path.append("Frequent small claims detected → REVIEW")
            reasons.append("Suspicious frequent small expense pattern.")
            return "REVIEW", decision_path, reasons

        # Policy score 
        policy_score = self.calculate_policy_score(expense)
        decision_path.append(f"Policy compliance calculated = {policy_score:.0f}%")

        # Receipt check 
        if not expense["receipt_uploaded"]:
            decision_path.append("Receipt missing → REJECT")
            reasons.append("Receipt is mandatory.")
            return "REJECT", decision_path, reasons

        decision_path.append("Receipt uploaded → Continue")

        # Policy threshold 
        if policy_score < 60:
            decision_path.append("Policy compliance low → REJECT")
            reasons.append("Expense violates company policy.")
            return "REJECT", decision_path, reasons

        decision_path.append("Policy acceptable → Continue")

        # Monthly limit 
        if expense["monthly_expense_total"] > self.MONTHLY_LIMIT:
            decision_path.append("Monthly expense exceeded → REVIEW")
            reasons.append("Monthly expense exceeds allowed limit.")
            return "REVIEW", decision_path, reasons

        decision_path.append("Monthly expenses OK → Continue")

        # Category limit 
        limit = self.LEVEL_LIMITS[level][category]

        if expense["expense_amount"] > limit:
            decision_path.append("Expense exceeds category limit → REVIEW")
            reasons.append("Expense exceeds allowed limit for employee level.")
            return "REVIEW", decision_path, reasons

        # Final approval 
        self.store_receipt(expense["receipt_id"], expense)

        decision_path.append("All checks passed → APPROVE")
        reasons.append("Expense automatically approved.")

        return "APPROVE", decision_path, reasons
