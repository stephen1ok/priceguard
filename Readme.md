# PriceGuard

A console-based Python app that tracks personal expenses **and** tells you whether the price you just paid for an item is above or below what you've paid for it before.

## Why I Built This

Most expense trackers just record how much you spend. PriceGuard goes a step further — every time you log an expense, it compares the price you paid for that specific item against your own price history and tells you if you got a good deal or overpaid.

## Features

- **Add expenses** by category (e.g. food, transport, data) and item name (e.g. eggs, fuel)
- **Price comparison** — automatically checks new prices against past prices for the same item
- **Expense summary** — totals per category, and flags the highest-spending category
- **Item price check** — shows average, lowest, and highest price ever paid per item
- **Input validation** — rejects negative or non-numeric amounts
- **Data persistence** — all data is saved to `priceguard_data.json` so nothing is lost between sessions

## How to Run

1. Make sure you have Python 3 installed.
2. Download `priceguard.py`.
3. Open a terminal in the folder containing the file.
4. Run:
   ```
   python priceguard.py
   ```
   (On some systems, use `python3` instead of `python`.)

## Example Usage

```
=== PriceGuard ===
1. Add expense
2. View expense summary
3. View item price check
4. Exit
Choose an option (1-4): 1
Category (e.g. food, transport, data): food
Item name (e.g. eggs, fuel): eggs
Amount paid (₦): 3500
First time logging 'eggs'. Price saved as the starting average.
Expense added.
```

On the next entry for eggs, PriceGuard tells you whether the new price is above or below your average.

## How Data Is Stored

Data is saved in a file called `priceguard_data.json`, structured like this:

```json
{
  "expenses": {
    "food": [3500, 1200]
  },
  "item_prices": {
    "eggs": [3500]
  }
}
```

This file is created automatically the first time you add an expense.

## Built With

- Python 3
- Standard library only (`json`, `os`) — no external dependencies

## Possible Future Improvements

- Monthly spending limit with warnings
- Category-based price alerts
- Export summary to CSV
- Simple GUI or web version
