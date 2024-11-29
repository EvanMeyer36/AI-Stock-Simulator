import json
import yfinance as yf
from datetime import datetime

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

    def view_portfolio(self):
        performance = self.calculate_portfolio_performance()
        return {
            "balance": self.balance,
            "holdings": {ticker: details["shares"] for ticker, details in performance["current_holdings"].items()},
            "performance": performance
        }

    def add_money(self, amount):
        self.balance += amount
        self.save_account()

    def withdraw_money(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save_account()
        else:
            print("Insufficient balance!")