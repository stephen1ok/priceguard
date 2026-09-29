"""
PriceGuard
A console app that tracks your expenses AND tells you if the price
you paid for an item is above or below what you've paid before.

Data is saved to priceguard_data.json so it survives restarts.
"""

import json
import os

DATA_FILE = "priceguard_data.json"


def load_data():
    """Load expenses and item_prices from file, or start fresh."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("expenses", {}), data.get("item_prices", {})
    return {}, {}


def save_data(expenses, item_prices):
    """Save both dictionaries to file."""
    data = {"expenses": expenses, "item_prices": item_prices}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_valid_amount(prompt):
    """Keep asking until the user enters a valid positive number."""
    while True:
        raw = input(prompt)
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be greater than zero. Try again.")
                continue
            return amount
        except ValueError:
            print("That's not a valid number. Try again.")


def average_price(item_prices, item):
    """Return the average price paid for an item."""
    prices = item_prices[item]
    return sum(prices) / len(prices)


def add_expense(expenses, item_prices):
    category = input("Category (e.g. food, transport, data): ").strip().lower()
    item = input("Item name (e.g. eggs, fuel): ").strip().lower()
    amount = get_valid_amount("Amount paid (₦): ")

    # Add to expenses by category
    expenses.setdefault(category, []).append(amount)

    # Compare against past prices for this item BEFORE adding the new one
    if item in item_prices and len(item_prices[item]) > 0:
        avg = average_price(item_prices, item)
        if amount > avg:
            diff = amount - avg
            print(f"You paid ₦{amount:.2f}. That's ₦{diff:.2f} ABOVE "
                  f"the average of ₦{avg:.2f} for {item}.")
        elif amount < avg:
            diff = avg - amount
            print(f"You paid ₦{amount:.2f}. That's ₦{diff:.2f} BELOW "
                  f"the average of ₦{avg:.2f} for {item}. Good price!")
        else:
            print(f"You paid exactly the average price of ₦{avg:.2f} for {item}.")
    else:
        print(f"First time logging '{item}'. Price saved as the starting average.")

    # Now add the new price to the item's history
    item_prices.setdefault(item, []).append(amount)

    print("Expense added.\n")


def view_expense_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print("\n--- Expense Summary ---")
    totals = {}
    for category, amounts in expenses.items():
        total = sum(amounts)
        totals[category] = total
        print(f"{category.capitalize():15} ₦{total:.2f}")

    highest_category = max(totals, key=totals.get)
    print(f"\nHighest spending category: {highest_category.capitalize()} "
          f"(₦{totals[highest_category]:.2f})\n")


def view_item_prices(item_prices):
    if not item_prices:
        print("No item prices recorded yet.\n")
        return

    print("\n--- Item Price Check ---")
    for item, prices in item_prices.items():
        avg = sum(prices) / len(prices)
        lowest = min(prices)
        highest = max(prices)
        print(f"{item.capitalize():15} avg ₦{avg:.2f}  "
              f"(lowest ₦{lowest:.2f}, highest ₦{highest:.2f}, "
              f"{len(prices)} entries)")
    print()


def main():
    expenses, item_prices = load_data()

    while True:
        print("=== PriceGuard ===")
        print("1. Add expense")
        print("2. View expense summary")
        print("3. View item price check")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses, item_prices)
            save_data(expenses, item_prices)
        elif choice == "2":
            view_expense_summary(expenses)
        elif choice == "3":
            view_item_prices(item_prices)
        elif choice == "4":
            save_data(expenses, item_prices)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Pick 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()