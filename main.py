from rule_engine import ApprovalEngine
import sys


EXPENSE_MENU = {
    "1": "food",
    "2": "accommodation",
    "3": "travel",
    "4": "transport",
    "5": "office_supplies",
    "6": "training",
    "7": "client_meeting"
}


def reject_and_exit(message):
    print("\nInput Rejected")
    print("----------------")
    print("Reason:", message)
    sys.exit()


def get_user_input():
    print("\nEnter Expense Details")
    print("----------------------")

    employee_id = input("Employee ID : ").strip()
    if not employee_id:
        reject_and_exit("Employee ID cannot be empty.")

    print("\nSelect Expense Type:")
    print("1. Food")
    print("2. Accommodation")
    print("3. Travel")
    print("4. Transport")
    print("5. Office Supplies")
    print("6. Training")
    print("7. Client Meeting")

    expense_choice = input("Enter choice number: ").strip()

    if expense_choice not in EXPENSE_MENU:
        reject_and_exit("Invalid expense choice.")

    expense_type = EXPENSE_MENU[expense_choice]

    amount_input = input("Expense Amount: ").strip()
    if not amount_input:
        reject_and_exit("Expense amount required.")

    expense_amount = float(amount_input)

    monthly_input = input("Monthly Expense Total: ").strip()
    if not monthly_input:
        reject_and_exit("Monthly total required.")

    monthly_expense_total = float(monthly_input)

    receipt_input = input("Receipt Available? (yes/no): ").strip().lower()

    if receipt_input not in ["yes", "no"]:
        reject_and_exit("Enter yes or no for receipt.")

    receipt_uploaded = receipt_input == "yes"

    receipt_id = None
    if receipt_uploaded:
        receipt_id = input("Receipt ID: ").strip()
        if not receipt_id:
            reject_and_exit("Receipt ID required.")

    return {
        "employee_id": employee_id,
        "expense_type": expense_type,
        "expense_amount": expense_amount,
        "monthly_expense_total": monthly_expense_total,
        "receipt_uploaded": receipt_uploaded,
        "receipt_id": receipt_id
    }


def main():
    engine = ApprovalEngine()

    expense_data = get_user_input()

    decision, path, reasons = engine.evaluate(expense_data)

    print("\nExpense Approval Result")
    print("------------------------")
    print("Decision:", decision)

    print("\nDecision Path:")
    for step in path:
        print("-", step)

    print("\nReason Summary:")
    for r in reasons:
        print("-", r)


if __name__ == "__main__":
    main()
