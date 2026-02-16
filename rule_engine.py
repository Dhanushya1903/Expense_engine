import json
import os


class ApprovalEngine:

    RECEIPT_FILE = "receipts.json"
    REVIEW_FILE = "reviews.json"
    REJECTION_FILE = "rejections.json"
    EMPLOYEE_FILE = "employees.json"

    LEVEL_LIMITS = {
        "L1": {
            "food": 1500,
            "accommodation": 6000,
            "travel": 8000,
            "transport": 2000,
            "office_supplies": 2500,
            "training": 5000,
            "client_meeting": 3000
        },
        "L2": {
            "food": 2000,
            "accommodation": 8000,
            "travel": 10000,
            "transport": 3000,
            "office_supplies": 3500,
            "training": 8000,
            "client_meeting": 5000
        },
        "L3": {
            "food": 3000,
            "accommodation": 12000,
            "travel": 15000,
            "transport": 5000,
            "office_supplies": 5000,
            "training": 12000,
            "client_meeting": 8000
        }
    }

    MONTHLY_LIMIT = 50000

    # -------------------------
    # Generic file loader
    # -------------------------
    def load_file(self, file, default):
        if not os.path.exists(file):
            return default

        with open(file, "r") as f:
            return json.load(f)

    def save_file(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=2)

    # -------------------------
    # Get employee level
    # -------------------------
    def get_employee_level(self, employee_id):
        data = self.load_file(self.EMPLOYEE_FILE, {"employees": {}})
        employees = data.get("employees", {})
        return employees.get(employee_id)

    # -------------------------
    # Duplicate receipt check
    # -------------------------
    def is_duplicate_receipt(self, receipt_id):
        data = self.load_file(self.RECEIPT_FILE,
                              {"used_receipts": [], "expense_history": []})
        return receipt_id in data["used_receipts"]

    # -------------------------
    # Store approved expense
    # -------------------------
    def store_approved(self, receipt_id, expense):
        data = self.load_file(self.RECEIPT_FILE,
                              {"used_receipts": [], "expense_history": []})

        data["used_receipts"].append(receipt_id)
        data["expense_history"].append(expense)

        self.save_file(self.RECEIPT_FILE, data)

    # -------------------------
    # Store review expense
    # -------------------------
    def store_review(self, expense, reasons):
        data = self.load_file(self.REVIEW_FILE, {"reviews": []})

        record = expense.copy()
        record["reasons"] = reasons

        data["reviews"].append(record)
        self.save_file(self.REVIEW_FILE, data)

    # -------------------------
    # Store rejected expense
    # -------------------------
    def store_rejection(self, expense, reasons):
        data = self.load_file(self.REJECTION_FILE, {"rejections": []})

        record = expense.copy()
        record["reasons"] = reasons

        data["rejections"].append(record)
        self.save_file(self.REJECTION_FILE, data)

    # -------------------------
    # Fraud detection
    # -------------------------
    def frequent_small_claims(self, employee_id):
        data = self.load_file(self.RECEIPT_FILE,
                              {"used_receipts": [], "expense_history": []})

        small_claims = [
            e for e in data["expense_history"]
            if e["employee_id"] == employee_id
            and e["expense_amount"] < 2000
        ]

        return len(small_claims) >= 5

    # -------------------------
    # Policy compliance score
    # -------------------------
    def calculate_policy_score(self, expense):
        total_rules = 4
        passed = 0

        level = expense["employee_level"]
        category = expense["expense_type"]

        if expense["receipt_uploaded"]:
            passed += 1

        if category in self.LEVEL_LIMITS[level]:
            passed += 1

        limit = self.LEVEL_LIMITS[level][category]

        if expense["expense_amount"] <= limit:
            passed += 1

        if expense["monthly_expense_total"] <= self.MONTHLY_LIMIT:
            passed += 1

        return (passed / total_rules) * 100

    # -------------------------
    # Decision engine
    # -------------------------
    def evaluate(self, expense):

        decision_path = []
        reasons = []

        employee_id = expense["employee_id"]

        level = self.get_employee_level(employee_id)

        if level is None:
            reasons.append("Employee not found.")
            self.store_rejection(expense, reasons)
            return "REJECT", ["Invalid employee"], reasons

        expense["employee_level"] = level
        category = expense["expense_type"]

        decision_path.append(f"Employee level detected: {level}")

        if expense["expense_amount"] <= 0:
            reasons.append("Expense must be positive.")
            self.store_rejection(expense, reasons)
            return "REJECT", ["Invalid expense"], reasons

        if category not in self.LEVEL_LIMITS[level]:
            reasons.append("Unsupported expense category.")
            self.store_rejection(expense, reasons)
            return "REJECT", ["Invalid category"], reasons

        if expense["receipt_uploaded"] and \
                self.is_duplicate_receipt(expense["receipt_id"]):
            decision_path.append("Duplicate receipt → REJECT")
            reasons.append("Receipt already used.")
            self.store_rejection(expense, reasons)
            return "REJECT", decision_path, reasons

        decision_path.append("Receipt ID unique")

        if self.frequent_small_claims(employee_id):
            decision_path.append("Frequent small claims → REVIEW")
            reasons.append("Suspicious frequent small claims.")
            self.store_review(expense, reasons)
            return "REVIEW", decision_path, reasons

        policy_score = self.calculate_policy_score(expense)
        decision_path.append(f"Policy score = {policy_score:.0f}%")

        if not expense["receipt_uploaded"]:
            decision_path.append("Receipt missing → REJECT")
            reasons.append("Receipt required.")
            self.store_rejection(expense, reasons)
            return "REJECT", decision_path, reasons

        if policy_score < 60:
            decision_path.append("Policy violation → REJECT")
            reasons.append("Policy violation.")
            self.store_rejection(expense, reasons)
            return "REJECT", decision_path, reasons

        if expense["monthly_expense_total"] > self.MONTHLY_LIMIT:
            decision_path.append("Monthly limit exceeded → REVIEW")
            reasons.append("Monthly expense exceeds limit.")
            self.store_review(expense, reasons)
            return "REVIEW", decision_path, reasons

        limit = self.LEVEL_LIMITS[level][category]

        if expense["expense_amount"] > limit:
            decision_path.append("Category limit exceeded → REVIEW")
            reasons.append("Expense exceeds allowed limit.")
            self.store_review(expense, reasons)
            return "REVIEW", decision_path, reasons

        self.store_approved(expense["receipt_id"], expense)

        decision_path.append("All checks passed → APPROVE")
        reasons.append("Expense approved automatically.")

        return "APPROVE", decision_path, reasons
