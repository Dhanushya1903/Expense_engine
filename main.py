from rule_engine import ApprovalEngine


def get_user_input():
    print("\nEnter Expense Details")
    print("----------------------")

    employee_id = input("Employee ID (E101–E400): ")

    expense_type = input("Expense Type (travel/food/hotel): ")

    expense_amount = float(input("Expense Amount: "))
    monthly_expense_total = float(input("Monthly Expense Total: "))

    receipt_input = input("Receipt Available? (yes/no): ").strip().lower()
    receipt_uploaded = receipt_input == "yes"

    receipt_id = input("Receipt ID: ")

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