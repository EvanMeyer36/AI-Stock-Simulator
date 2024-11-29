import json

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
            # If the file doesn't exist, start fresh
            print("No previous account data found. Starting fresh.")

    def add_money(self, amount):
        self.balance += amount
        self.save_account()

    def withdraw_money(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save_account()
        else:
            print("Insufficient balance!")

    def buy_stock(self, ticker, price, quantity):
        total_cost = price * quantity
        if total_cost <= self.balance:
            self.balance -= total_cost
            self.holdings[ticker] = self.holdings.get(ticker, 0) + quantity
            self.save_account()
        else:
            print("Insufficient balance to buy stocks!")

    def sell_stock(self, ticker, price, quantity):
        if ticker in self.holdings and self.holdings[ticker] >= quantity:
            self.holdings[ticker] -= quantity
            self.balance += price * quantity
            if self.holdings[ticker] == 0:
                del self.holdings[ticker]
            self.save_account()
        else:
            print("You don't own enough of this stock!")

    def view_portfolio(self):
        return {"balance": self.balance, "holdings": self.holdings}