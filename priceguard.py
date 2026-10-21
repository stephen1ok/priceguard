"""
PriceGuard (v2)
A console app that tracks your expenses, compares prices against your
own history, and now lets you view, edit, and delete individual entries.

Each expense is stored as one record with a unique ID:
{"id": 1, "category": "food", "item": "eggs", "amount": 3500}

Data is saved to priceguard_data.json so it survives restarts.
"""

import json
import os

DATA_FILE = "priceguard_data.json"


def load_data():
    """Load the list of expense records from file, or start fresh."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("records", [])
    return []


def save_data(records):
    """Save the records list to file."""
    with open(DATA_FILE, "w") as f:
        json.dump({"records": records}, f, indent=2)


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


def next_id(records):
    """Work out the next unique ID to use for a new record."""
    if not records:
        return 1
    return max(record["id"] for record in records) + 1


def average_price_for_item(records, item):
    """Return the average amount paid for a given item, or None if never logged."""
    prices = [r["amount"] for r in records if r["item"] == item]
    if not prices:
        return None
    return sum(prices) / len(prices)


def add_expense(records):
    category = input("Category (e.g. food, transport, data): ").strip().lower()
    item = input("Item name (e.g. eggs, fuel): ").strip().lower()
    amount = get_valid_amount("Amount paid (\u20a6): ")

    # Compare against past prices for this item BEFORE adding the new one
    avg = average_price_for_item(records, item)
    if avg is not None:
        if amount > avg:
            diff = amount - avg
            print(f"You paid \u20a6{amount:.2f}. That's \u20a6{diff:.2f} ABOVE "
                  f"the average of \u20a6{avg:.2f} for {item}.")
        elif amount < avg:
            diff = avg - amount
            print(f"You paid \u20a6{amount:.2f}. That's \u20a6{diff:.2f} BELOW "
                  f"the average of \u20a6{avg:.2f} for {item}. Good price!")
        else:
            print(f"You paid exactly the average price of \u20a6{avg:.2f} for {item}.")
    else:
        print(f"First time logging '{item}'. Price saved as the starting average.")

    record = {
        "id": next_id(records),
        "category": category,
        "item": item,
        "amount": amount,
    }
    records.append(record)
    print(f"Expense added with ID {record['id']}.\n")


def view_all_entries(records):
    if not records:
        print("No entries recorded yet.\n")
        return

    print("\n--- All Entries ---")
    print(f"{'ID':4} {'Category':15} {'Item':15} {'Amount':>10}")
    for r in records:
        print(f"{r['id']:<4} {r['category'].capitalize():15} "
              f"{r['item'].capitalize():15} \u20a6{r['amount']:>8.2f}")
    print()


def find_entry(records, entry_id):
    """Return the record with this ID, or None if not found."""
    for r in records:
        if r["id"] == entry_id:
            return r
    return None


def get_valid_id(prompt):
    """Keep asking until the user enters a valid whole number ID."""
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid whole number ID.")


def delete_entry(records):
    if not records:
        print("No entries to delete.\n")
        return

    view_all_entries(records)
    entry_id = get_valid_id("Enter the ID of the entry to delete: ")
    record = find_entry(records, entry_id)

    if record is None:
        print(f"No entry found with ID {entry_id}.\n")
        return

    print(f"Entry {entry_id}: {record['category']} / {record['item']} "
          f"/ \u20a6{record['amount']:.2f}")
    confirm = input("Are you sure you want to delete this? (y/n): ").strip().lower()

    if confirm == "y":
        records.remove(record)
        print("Entry deleted.\n")
    else:
        print("Cancelled. Nothing was deleted.\n")


def edit_entry(records):
    if not records:
        print("No entries to edit.\n")
        return

    view_all_entries(records)
    entry_id = get_valid_id("Enter the ID of the entry to edit: ")
    record = find_entry(records, entry_id)

    if record is None:
        print(f"No entry found with ID {entry_id}.\n")
        return

    print(f"Editing entry {entry_id}. Press Enter to keep the current value.")

    new_category = input(f"Category [{record['category']}]: ").strip().lower()
    if new_category:
        record["category"] = new_category

    new_item = input(f"Item [{record['item']}]: ").strip().lower()
    if new_item:
        record["item"] = new_item

    new_amount = input(f"Amount [\u20a6{record['amount']:.2f}]: ").strip()
    if new_amount:
        try:
            value = float(new_amount)
            if value > 0:
                record["amount"] = value
            else:
                print("Amount must be greater than zero. Amount not changed.")
        except ValueError:
            print("That's not a valid number. Amount not changed.")

    print("Entry updated.\n")


def view_expense_summary(records):
    if not records:
        print("No expenses recorded yet.\n")
        return

    print("\n--- Expense Summary ---")
    totals = {}
    for r in records:
        totals[r["category"]] = totals.get(r["category"], 0) + r["amount"]

    for category, total in totals.items():
        print(f"{category.capitalize():15} \u20a6{total:.2f}")

    highest_category = max(totals, key=totals.get)
    print(f"\nHighest spending category: {highest_category.capitalize()} "
          f"(\u20a6{totals[highest_category]:.2f})\n")


def view_item_prices(records):
    if not records:
        print("No item prices recorded yet.\n")
        return

    items = {}
    for r in records:
        items.setdefault(r["item"], []).append(r["amount"])

    print("\n--- Item Price Check ---")
    for item, prices in items.items():
        avg = sum(prices) / len(prices)
        lowest = min(prices)
        highest = max(prices)
        print(f"{item.capitalize():15} avg \u20a6{avg:.2f}  "
              f"(lowest \u20a6{lowest:.2f}, highest \u20a6{highest:.2f}, "
              f"{len(prices)} entries)")
    print()


def main():
    records = load_data()

    while True:
        print("=== PriceGuard ===")
        print("1. Add expense")
        print("2. View expense summary")
        print("3. View item price check")
        print("4. View all entries")
        print("5. Edit an entry")
        print("6. Delete an entry")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense(records)
            save_data(records)
        elif choice == "2":
            view_expense_summary(records)
        elif choice == "3":
            view_item_prices(records)
        elif choice == "4":
            view_all_entries(records)
        elif choice == "5":
            edit_entry(records)
            save_data(records)
        elif choice == "6":
            delete_entry(records)
            save_data(records)
        elif choice == "7":
            save_data(records)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Pick a number from 1 to 7.\n")


if __name__ == "__main__":
    main()