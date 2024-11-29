import json
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
class Account:
    def __init__(self, initial_balance=10000, file_path="account_data.json"):
        self.file_path = file_path
        self.balance = initial_balance
        self.holdings = {}
        self.load_account()

    def save_account(self):
        data = {
            "balance": self.balance,
            "holdings": self.holdings
        }
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def load_account(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.balance = data["balance"]
                self.holdings = data["holdings"]
        except FileNotFoundError:
            print("No previous account data found. Starting fresh.")

    def buy_stock(self, ticker, price, quantity):
        total_cost = price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            
            # Track purchase details
            if ticker not in self.holdings:
                self.holdings[ticker] = {
                    "shares": quantity,
                    "avg_price": price,
                    "total_cost": total_cost,
                    "purchase_dates": [datetime.now().isoformat()]
                }
            else:
                # Update average price and total shares
                existing_shares = self.holdings[ticker]["shares"]
                existing_cost = self.holdings[ticker]["total_cost"]
                
                new_total_shares = existing_shares + quantity
                new_total_cost = existing_cost + total_cost
                new_avg_price = new_total_cost / new_total_shares
                
                self.holdings[ticker].update({
                    "shares": new_total_shares,
                    "avg_price": new_avg_price,
                    "total_cost": new_total_cost,
                    "purchase_dates": self.holdings[ticker]["purchase_dates"] + [datetime.now().isoformat()]
                })
            
            self.save_account()
        else:
            print("Insufficient balance to buy stocks!")

    def sell_stock(self, ticker, price, quantity):
        if ticker in self.holdings and self.holdings[ticker]["shares"] >= quantity:
            holding = self.holdings[ticker]
            
            # Calculate profit/loss
            avg_price = holding["avg_price"]
            total_sale_value = price * quantity
            total_cost_basis = avg_price * quantity
            profit_loss = total_sale_value - total_cost_basis

            # Update holdings
            holding["shares"] -= quantity
            self.balance += total_sale_value

            # Remove ticker if no shares left
            if holding["shares"] == 0:
                del self.holdings[ticker]
            
            self.save_account()
            
            print(f"Sold {quantity} shares of {ticker}")
            print(f"Sale value: ${total_sale_value:.2f}")
            print(f"Cost basis: ${total_cost_basis:.2f}")
            print(f"Profit/Loss: ${profit_loss:.2f}")
        else:
            print("You don't own enough of this stock!")

    def calculate_portfolio_performance(self):
        total_portfolio_value = self.balance
        performance_details = {"current_holdings": {}}

        for ticker, holding in self.holdings.items():
            try:
                current_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
                current_value = current_price * holding["shares"]
                total_portfolio_value += current_value

                performance_details["current_holdings"][ticker] = {
                    "shares": holding["shares"],
                    "avg_cost": holding["avg_price"],
                    "current_price": current_price,
                    "total_cost": holding["total_cost"],
                    "current_value": current_value,
                    "profit_loss": current_value - holding["total_cost"],
                    "return_percentage": ((current_value - holding["total_cost"]) / holding["total_cost"]) * 100
                }
            except Exception as e:
                print(f"Error calculating performance for {ticker}: {e}")

        performance_details["total_balance"] = self.balance
        performance_details["total_portfolio_value"] = total_portfolio_value
        performance_details["total_return_percentage"] = ((total_portfolio_value - sum(h["total_cost"] for h in self.holdings.values())) / sum(h["total_cost"] for h in self.holdings.values())) * 100 if self.holdings else 0

        return performance_details

    def plot_stock_performance(self, ticker, period='1mo'):
        """
        Generate a stock performance graph for a specific ticker
        
        Args:
            ticker (str): Stock ticker symbol
            period (str): Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
        
        Returns:
            str: Path to saved graph image
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                print(f"No historical data available for {ticker}")
                return None

            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(hist.index, hist['Close'], label=f'{ticker} Close Price')
            plt.title(f'{ticker} Stock Performance - {period}')
            plt.xlabel('Date')
            plt.ylabel('Price (USD)')
            plt.legend()
            plt.grid(True)
            
            # Rotate and align the tick labels so they look better
            plt.gcf().autofmt_xdate()
            
            # Save the plot
            filename = f"{ticker}_performance_{period}.png"
            plt.savefig(filename)
            plt.close()
            
            return filename
        
        except Exception as e:
            print(f"Error plotting stock performance for {ticker}: {e}")
            return None

    def generate_portfolio_performance_graph(self):
        """
        Generate a graph showing portfolio value over time
        
        Returns:
            str: Path to saved graph image
        """
        try:
            # Collect historical data for all holdings
            portfolio_history = {}
            for ticker in self.holdings.keys():
                stock = yf.Ticker(ticker)
                hist = stock.history(period='1mo')
                
                if not hist.empty:
                    portfolio_history[ticker] = hist['Close']
            
            # Create the plot
            plt.figure(figsize=(12, 7))
            
            for ticker, prices in portfolio_history.items():
                plt.plot(prices.index, prices, label=ticker)
            
            plt.title('Portfolio Stock Performance')
            plt.xlabel('Date')
            plt.ylabel('Price (USD)')
            plt.legend()
            plt.grid(True)
            plt.gcf().autofmt_xdate()
            
            # Save the plot
            filename = "portfolio_performance.png"
            plt.savefig(filename)
            plt.close()
            
            return filename
        
        except Exception as e:
            print(f"Error generating portfolio performance graph: {e}")
            return None

    # Add this method to the view_portfolio method
    def view_portfolio(self):
        performance = self.calculate_portfolio_performance()
        stock_graphs = {ticker: self.plot_stock_performance(ticker) for ticker in self.holdings.keys()}
        portfolio_graph = self.generate_portfolio_performance_graph()

        # Format output
        print("\nYour Portfolio Summary:")
        print("-------------------------")
        print(f"Balance: ${self.balance:,.2f}\n")

        if self.holdings:
            print("Holdings:")
            for ticker, details in performance["current_holdings"].items():
                print(f"  - {ticker}: ")
                print(f"    - Shares: {details['shares']}")
                print(f"    - Average Cost: ${details['avg_cost']:.2f}")
                print(f"    - Current Price: ${details['current_price']:.2f}")
                print(f"    - Total Cost: ${details['total_cost']:.2f}")
                print(f"    - Current Value: ${details['current_value']:.2f}")
                print(f"    - Profit/Loss: ${details['profit_loss']:.2f} ({details['return_percentage']:.2f}%)\n")
        else:
            print("No holdings yet.\n")

        print(f"Total Portfolio Value: ${performance['total_portfolio_value']:.2f}")
        print(f"Total Return Percentage: {performance['total_return_percentage']:.2f}%\n")

        print("Graphs:")
        for ticker, graph in stock_graphs.items():
            print(f"  - {ticker} Performance: {graph}")
        print(f"  - Portfolio Performance: {portfolio_graph}")
        print("-------------------------\n")

    def add_money(self, amount):
        self.balance += amount
        self.save_account()

    def withdraw_money(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save_account()
        else:
            print("Insufficient balance!")