"""
Currency Converter (Console Version with File Handling)
Fetches live exchange rates from open.er-api.com
Saves conversion history in a file
Run with: python currency_converter.py
"""

import urllib.request
import json

API_URL = "https://open.er-api.com/v6/latest/{base}"


# ── Fetch Rates ───────────────────────────────────────────────
def fetch_rates(base: str) -> dict:
    url = API_URL.format(base=base.upper())
    with urllib.request.urlopen(url, timeout=8) as response:
        data = json.loads(response.read())

    if data.get("result") != "success":
        raise ValueError("API error")

    return data["rates"]


# ── Convert Function ──────────────────────────────────────────
def convert_currency(amount, from_currency, to_currency):
    rates = fetch_rates(from_currency)

    if to_currency not in rates:
        return "Invalid currency"

    rate = rates[to_currency]
    return amount * rate


# ── Save History (File Handling) ──────────────────────────────
def save_history(amount, from_curr, to_curr, result):
    with open("history.txt", "a") as file:
        file.write(f"{amount} {from_curr} = {result:.4f} {to_curr}\n")


# ── View History (File Handling) ──────────────────────────────
def view_history():
    try:
        with open("history.txt", "r") as file:
            print("\n📜 Conversion History:\n")
            content = file.read()
            if content.strip() == "":
                print("No history yet.")
            else:
                print(content)
    except FileNotFoundError:
        print("\nNo history file found yet.")


# ── Clear History (Extra Feature) ─────────────────────────────
def clear_history():
    with open("history.txt", "w") as file:
        file.write("")  # overwrite file
    print("✅ History cleared!")


# ── Main Program ──────────────────────────────────────────────
def main():
    while True:
        print("\n💱 Currency Converter (Live Rates)\n")
        print("1. Convert Currency")
        print("2. View History")
        print("3. Clear History")
        print("4. Exit")

        choice = input("Choose option (1-4): ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))
                from_curr = input("From currency (e.g., USD, INR): ").upper()
                to_curr = input("To currency (e.g., EUR, INR): ").upper()

                result = convert_currency(amount, from_curr, to_curr)

                if isinstance(result, str):
                    print("❌", result)
                else:
                    print(f"\n✅ {amount} {from_curr} = {result:.4f} {to_curr}")
                    save_history(amount, from_curr, to_curr, result)

            except Exception as e:
                print("❌ Error:", e)

        elif choice == "2":
            view_history()

        elif choice == "3":
            clear_history()

        elif choice == "4":
            print("👋 Exiting program...")
            break

        else:
            print("❌ Invalid choice, try again.")


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    main()