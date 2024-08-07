import pandas as pd
from datetime import datetime, timedelta

class UserAccount:
    def __init__(self, name, age, account_number, balance, income, expenses, investments, transactions_file):
        self.name = name
        self.age = age
        self.account_number = account_number
        self.balance = balance
        self.income = income
        self.expenses = expenses
        self.investments = investments
        self.transactions = self.process_transactions(transactions_file)
    
    def process_transactions(self, file_path):
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['TransDate'])
        return df

    def get_financial_summary(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        recent_transactions = self.transactions[(self.transactions['Date'] >= start_date) & (self.transactions['Date'] <= end_date)]
        total_spent = recent_transactions[recent_transactions['TransAmount'] < 0]['TransAmount'].sum()
        top_categories = recent_transactions.groupby('CategoryName')['TransAmount'].sum().sort_values(ascending=False).head(3)

        return f"""
        Name: {self.name}
        Age: {self.age}
        Account Number: {self.account_number}
        Current Balance: ${self.balance:,.2f}
        Monthly Income: ${self.income:,.2f}
        Monthly Expenses: ${self.expenses:,.2f}
        Current Investments: {', '.join(f'{k}: ${v:,.2f}' for k, v in self.investments.items())}
        
        Recent Financial Activity (Last 30 Days):
        Total Spent: ${abs(total_spent):,.2f}
        Top Spending Categories:
        {top_categories.to_string()}
        """

    def get_transaction_data(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        last_transactions = self.transactions[(self.transactions['Date'] >= start_date) & (self.transactions['Date'] <= end_date)]
        last_transactions = last_transactions.drop(columns=['Unnamed: 0'])
        transactions_str = last_transactions.to_string(index=False)
        return f"Transaction History:\n{transactions_str}"

    def add_transaction(self, transaction):
        
        new_transaction = pd.DataFrame([{
            'TransDate': transaction['date'],
            'Cif':'R001729580',
            'TransNarration': f"Transfer to {transaction['receiverBank']}",
            'CategoryName': transaction['category'],
            'TransAmount': transaction['amount'],
            'Date': pd.to_datetime(transaction['date'])
        }])
        
        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        self.transactions = self.transactions.sort_values('Date', ascending=False).reset_index(drop=True)

    def update_balance(self, amount):
        self.balance += amount
        return self.balance

    def get_transactions(self, limit=10):
        self.transactions = self.transactions.sort_values('Date', ascending=False).reset_index(drop=True)
        return self.transactions.head(limit).to_dict('records')
    
    def create_savings_plan(self, amount, duration, savings_type):
        if savings_type not in ['locked', 'flexible']:
            raise ValueError("Savings type must be either 'locked' or 'flexible'")
        
        if amount <= 0 or duration <= 0:
            raise ValueError("Amount and duration must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds for savings plan")
        
        new_savings_plan = {
            'type': savings_type,
            'amount': amount,
            'duration': duration,
            'start_date': datetime.now().strftime("%Y-%m-%d"),
            'end_date': (datetime.now() + timedelta(days=duration*30)).strftime("%Y-%m-%d"),
            'current_balance': 0
        }
        
        if 'savings_plans' not in self.__dict__:
            self.savings_plans = []
        
        self.savings_plans.append(new_savings_plan)
        self.update_balance(-amount)
        
        return new_savings_plan

# # Create a simulated user account
# user = UserAccount(
#     name="Alice Johnson",
#     age=28,
#     account_number="1234567890",
#     balance=15000.00,
#     income=5000.00,
#     expenses=3500.00,
#     investments={"Stocks": 5000.00, "Bonds": 2000.00, "ETFs": 3000.00},
#     transactions_file="Michael_data.csv"  # Replace with your actual file path
# )