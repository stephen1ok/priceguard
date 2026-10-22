PriceGuard

A personal expense-tracking desktop application built with Python, PyQt5, and Qt Designer. PriceGuard helps users record expenses, organize spending by category, and compare item prices with their previous purchases.

Why I Built This

Many expense trackers only record how much you spend. PriceGuard aims to go a step further by tracking the prices of individual items over time, helping users understand their spending habits and notice when prices increase.

Features

- Expense entry form — enter an expense category, item name, and amount.
- View all entries — access recorded expenses.
- Edit expenses — update existing expense records.
- Delete expenses — remove unwanted entries.
- Price comparison — compare an item's current price with its previous prices.
- Expense summary — review spending by category and identify high-spending categories.
- Input validation — check expense amounts to prevent invalid entries.
- Data persistence — planned integration for saving expense records between sessions.

Note: Some features are still being connected and tested as development continues.

User Interface

PriceGuard is being developed as a desktop application using Qt Designer and PyQt5.

The current interface includes:

- A category input field.
- An item input field.
- An amount input field.
- A View All Entries button.
- An Add Expense button.
- An Edit an Entry button.
- A Delete an Entry button.
- An Exit button.

Technologies Used

- Python 3 — application logic.
- PyQt5 — desktop application interface.
- Qt Designer — visual interface design.
- JSON and OS modules — for file handling and data storage as the application is developed.

Project Structure

PriceGuard/
├── priceguard.py
├── priceguard.ui
├── priceguard_data.json
└── README.md

"priceguard_data.json" will be used for storing expense data when the data-saving functionality is integrated. The exact project structure may change as development continues.

How to Run

1. Install Python 3.

2. Install PyQt5 if it is not already installed:
   
   pip install PyQt5

3. Make sure "priceguard.py" and "priceguard.ui" are in the correct project locations.

4. Open a terminal in the project folder.

5. Run the application:
   
   python priceguard.py

How It Works

1. Enter the expense category.
2. Enter the name of the item.
3. Enter the amount paid.
4. Click Add Expense to record the expense.
5. Use the other buttons to view, edit, or delete entries as those functions are completed.

Current Development Status

The project has progressed from a console-based application to a graphical desktop interface.

Completed or started tasks include:

- Designed the desktop interface in Qt Designer.
- Loaded the ".ui" file into Python using PyQt5.
- Added category, item, and amount input fields.
- Connected the Exit button.
- Started connecting the expense management buttons and their functions.

Further testing and development are ongoing.

Future Improvements

- Complete the View All Entries, Edit, and Delete functions.
- Finish expense validation and error handling.
- Integrate JSON-based data saving and loading.
- Implement price history comparisons.
- Add expense summaries and spending alerts.
- Improve the interface layout and appearance.
- Add monthly spending limits.
- Support exporting expense reports to CSV.

Author

Okpor Stephen

Project Goal

To build a simple and useful desktop application that helps users manage personal expenses and make better spending decisions through item price tracking.