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
        print("Invalid input format.")
        sys.exit()

    return data["expense"]


def save_output(input_file, decision, path, reasons, expense):
    os.makedirs("outputs", exist_ok=True)

    base_name = os.path.basename(input_file)
    name_without_ext = os.path.splitext(base_name)[0]

    output_file = f"outputs/{name_without_ext}_output.json"

    result = {
        "decision": decision,
        "decision_path": path,
        "reasons": reasons,
        "expense": expense
    }

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print("\nOutput stored in:", output_file)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.json>")
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

    save_output(input_file, decision, path, reasons, expense_data)


if __name__ == "__main__":
    main()
