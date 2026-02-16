from rule_engine import ApprovalEngine
import json
import sys
import os


def load_input_file(file_path):
    if not os.path.exists(file_path):
        print("Input file not found:", file_path)
        sys.exit()

    with open(file_path, "r") as f:
        data = json.load(f)

    if "expense" not in data:
        print("Invalid input format. 'expense' field missing.")
        sys.exit()

    return data["expense"]


def main():
    # Check if file path provided
    if len(sys.argv) < 2:
        print("Usage:")
        print("python main.py <input_file.json>")
        sys.exit()

    input_file = sys.argv[1]

    expense_data = load_input_file(input_file)

    engine = ApprovalEngine()

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
