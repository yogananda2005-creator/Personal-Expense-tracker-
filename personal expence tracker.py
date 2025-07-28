import json
import matplotlib.pyplot as plt
from datetime import datetime

# File to store expenses
FILE_NAME = "expenses.json"

# Load existing expenses from file
def load_expenses():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file not found or corrupted

# Save all expenses to the file
def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)

# Add a new expense entry
def add_expense(expenses):
    try:
        amount = float(input("Enter amount (e.g., 50.0): ₹"))
        category = input("Enter category (Food, Transport, etc.): ")
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        date = date_input if date_input else datetime.today().strftime("%Y-%m-%d")

        # Create the expense record
        expense = {
            "amount": amount,
            "category": category,
            "date": date
        }

        # Append and save
        expenses.append(expense)
        save_expenses(expenses)
        print("✅ Expense added successfully!")
    except ValueError:
        print("❌ Invalid input. Amount must be a number.")

# Display a summary grouped by category
def view_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    total = 0
    category_totals = {}

    for exp in expenses:
        total += exp["amount"]
        cat = exp["category"]
        category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]

    print("\n📊 Expense Summary:")
    for category, amount in category_totals.items():
        print(f"- {category}: ₹{amount:.2f}")
    print(f"Total Spending: ₹{total:.2f}")

# Display all expenses with their index numbers
def display_expenses(expenses):
    if not expenses:
        print("No expenses to show.")
        return

    print("\n📄 List of Expenses:")
    for idx, exp in enumerate(expenses):
        print(f"{idx + 1}. ₹{exp['amount']} - {exp['category']} - {exp['date']}")

# Delete an expense by its index
def delete_expense(expenses):
    display_expenses(expenses)
    if not expenses:
        return

    try:
        index = int(input("Enter the expense number to delete: ")) - 1
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"✅ Deleted: ₹{removed['amount']} - {removed['category']} - {removed['date']}")
        else:
            print("❌ Invalid number.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Edit an existing expense
def edit_expense(expenses):
    display_expenses(expenses)
    if not expenses:
        return

    try:
        index = int(input("Enter the expense number to edit: ")) - 1
        if 0 <= index < len(expenses):
            exp = expenses[index]
            print(f"Editing: ₹{exp['amount']} - {exp['category']} - {exp['date']}")

            # Prompt for new values, retain old if blank
            new_amount = input(f"Enter new amount (or press Enter to keep ₹{exp['amount']}): ")
            new_category = input(f"Enter new category (or press Enter to keep {exp['category']}): ")
            new_date = input(f"Enter new date (or press Enter to keep {exp['date']}): ")

            if new_amount:
                exp['amount'] = float(new_amount)
            if new_category:
                exp['category'] = new_category
            if new_date:
                exp['date'] = new_date

            save_expenses(expenses)
            print("✅ Expense updated successfully!")
        else:
            print("❌ Invalid number.")
    except ValueError:
        print("❌ Please enter valid input.")

# Show a pie chart of expenses by category
def show_expense_graph(expenses):
    if not expenses:
        print("No expenses to display.")
        return

    # Calculate totals for each category
    category_totals = {}
    for exp in expenses:
        category = exp['category']
        amount = exp['amount']
        category_totals[category] = category_totals.get(category, 0) + amount

    # Prepare data for the pie chart
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')  # Equal aspect ratio = perfect circle
    plt.tight_layout()
    plt.show()

# Main menu loop
def main():
    expenses = load_expenses()

    while True:
        print("\n📌 Personal Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Show Expense Graph")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            show_expense_graph(expenses)
        elif choice == "6":
            print("👋 Exiting the program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main()
