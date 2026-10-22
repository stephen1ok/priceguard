import sys
import json
import os
from PyQt5 import QtWidgets, uic

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


class PriceGuardApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("priceguard.ui", self)

        self.exit_Button.clicked.connect(self.close)
        self.addButton.clicked.connect(self.add_expense)

        for button in self.findChildren(QtWidgets.QPushButton):
            text = button.text().lower()
            if "view all" in text:
                button.clicked.connect(self.show_all)
            elif "edit" in text:
                button.clicked.connect(self.edit_entry)
            elif "delete" in text:
                button.clicked.connect(self.delete_entry)

    def add_expense(self):
        category = self.categoryInput.text().strip().lower()
        item = self.itemInput.text().strip().lower()

        try:
            amount = float(self.amountInput.text())
        except ValueError:
            self.resultLabel.setText("Amount must be a number.")
            return

        if amount <= 0:
            self.resultLabel.setText("Amount must be greater than zero.")
            return

        records = load_data()
        records.append({"category": category, "item": item, "amount": amount})
        save_data(records)

        self.resultLabel.setText(f"Saved: {category}, {item}, ₦{amount:.2f}")

    def show_all(self):
        records = load_data()

        if not records:
            self.resultLabel.setText("No entries recorded yet.")
            return

        lines = ["--- All entries ---"]
        total = 0
        for number, r in enumerate(records, start=1):
            lines.append(f"{number}. {r['category'].capitalize()} | "
                         f"{r['item'].capitalize()} | ₦{r['amount']:.2f}")
            total += r["amount"]

        lines.append("")
        lines.append(f"Total: ₦{total:.2f}")

        self.resultLabel.setText("\n".join(lines))

    def edit_entry(self):
        records = load_data()

        if not records:
            self.resultLabel.setText("No entries to edit.")
            return

        number, ok = QtWidgets.QInputDialog.getInt(
            self, "Edit entry", "Entry number to edit:", 1, 1, len(records))
        if not ok:
            return

        record = records[number - 1]

        category, ok = QtWidgets.QInputDialog.getText(
            self, "Edit entry", "Category:", text=record["category"])
        if not ok:
            return

        item, ok = QtWidgets.QInputDialog.getText(
            self, "Edit entry", "Item:", text=record["item"])
        if not ok:
            return

        amount, ok = QtWidgets.QInputDialog.getDouble(
            self, "Edit entry", "Amount (₦):", record["amount"], 0.01, 100000000, 2)
        if not ok:
            return

        record["category"] = category.strip().lower()
        record["item"] = item.strip().lower()
        record["amount"] = amount
        save_data(records)

        self.show_all()

    def delete_entry(self):
        records = load_data()

        if not records:
            self.resultLabel.setText("No entries to delete.")
            return

        number, ok = QtWidgets.QInputDialog.getInt(
            self, "Delete entry", "Entry number to delete:", 1, 1, len(records))
        if not ok:
            return

        record = records[number - 1]

        answer = QtWidgets.QMessageBox.question(
            self, "Confirm delete",
            f"Delete {record['category']} | {record['item']} | "
            f"₦{record['amount']:.2f}?")
        if answer != QtWidgets.QMessageBox.Yes:
            return

        records.pop(number - 1)
        save_data(records)

        self.show_all()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PriceGuardApp()
    window.show()
    sys.exit(app.exec_())