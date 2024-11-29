from market_utils import get_stock_price, get_top_gainers, analyze_top_gainers
from ai_utils import suggest_investments, get_market_overview
from account_manager import Account
from colorama import Fore, Style, init
init(autoreset=True)

def print_menu():
    print(Fore.CYAN + "Welcome to Stock Trade Simulator!")
    print(Fore.GREEN + "\nMenu:")
    print(Fore.YELLOW + "1. View Portfolio")
    print(Fore.YELLOW + "2. Add Money")
    print(Fore.YELLOW + "3. Withdraw Money")
    print(Fore.YELLOW + "4. Buy Stock")
    print(Fore.YELLOW + "5. Sell Stock")
    print(Fore.YELLOW + "6. Get Investment Suggestions")
    print(Fore.YELLOW + "7. View Top Gainers")
    print(Fore.RED + "8. Exit")

def main():
    account = Account()
    print("Welcome to Stock Trade Simulator!")
    
    while True:
        print_menu()
        
        choice = input("Enter your choice: ")
        
        try:
            if choice == "1":
                print(account.view_portfolio())
            
            elif choice == "2":
                amount = float(input("Enter amount to add: "))
                account.add_money(amount)
            
            elif choice == "3":
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw_money(amount)
            
            elif choice == "4":
                ticker = input("Enter stock ticker: ").upper()
                price = get_stock_price(ticker)
                if price:
                    quantity = int(input(f"Current price of {ticker} is ${price:.2f}. Enter quantity to buy: "))
                    account.buy_stock(ticker, price, quantity)
            
            elif choice == "5":
                ticker = input("Enter stock ticker: ").upper()
                price = get_stock_price(ticker)
                if price:
                    quantity = int(input(f"Current price of {ticker} is ${price:.2f}. Enter quantity to sell: "))
                    account.sell_stock(ticker, price, quantity)
            
            elif choice == "6":  # Get Investment Suggestions
                gainers = get_top_gainers()
                if gainers:
                    market_data = get_market_overview(gainers)
                    portfolio = account.view_portfolio()
                    suggestions = suggest_investments(market_data, portfolio)
                    print("\nInvestment Suggestions:\n", suggestions)
                else:
                    print("No top gainers available at the moment.")
            
            elif choice == "7":  # View Top Gainers
                top_gainers = analyze_top_gainers()
                print("\nTop Gainers:")
                for gainer in top_gainers:
                    print(f"{gainer['Ticker']} - {gainer['Company Name']}")
                    print(f"  Current Price: ${gainer['Current Price']:.2f}")
                    print(f"  Percent Change: {gainer['Percent Change']:.2f}%\n")
            
            elif choice == "8":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Try again.")
        
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()