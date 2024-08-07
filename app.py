from flask import Flask, request, jsonify, render_template
from model import get_advice
from langchain.schema import HumanMessage, SystemMessage
from user import UserAccount
from datetime import datetime, timedelta

app = Flask(__name__)

# Create a simulated user account
user = UserAccount(
    name="Michael",
    age=22,
    account_number="0787845632",
    balance=100000.00,
    income=25000.00,
    expenses=15000.00,
    investments={"$BTC": 50000.00, "$ETH": 12000.00, "$SOL": 20000.00},
    transactions_file="Michael_data.csv"  # Replace with your actual file path
)

# Load the model and chain
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_query = request.form['query']
    print(user_query)
    financial_summary = user.get_financial_summary()
    transaction_data = user.get_transaction_data()
    print(f"Transaction Data: {transaction_data}")
    
    try:
        response = get_advice(user_query, financial_summary, transaction_data)
        print (response)
        return jsonify({'response': response})
    except Exception as e:
        print('failed')
        return jsonify({'error': str(e)})
    
@app.route('/send_money', methods=['POST'])
def send_money():
    data = request.json
    receiver_name = data['receiverName']
    receiver_bank = data['receiverBank']
    amount = float(data['amount'])
    category = data['category']

    if amount <= 0:
        return jsonify({'success': False, 'message': 'Invalid amount'})

    if amount > user.balance:
        return jsonify({'success': False, 'message': 'Insufficient funds'})

    # Perform the transaction
    new_balance = user.update_balance(-amount)
    transaction = {
        'date': datetime.now().strftime("%m/%d/20%y %H:%M"),
        'receiverName': receiver_name,
        'receiverBank': receiver_bank,
        'amount': amount,
        'category': category
    }
    user.add_transaction(transaction)

    return jsonify({
        'success': True,
        'newBalance': new_balance,
        'transaction': transaction
    })

@app.route('/get_transaction_history', methods=['GET'])
def get_transaction_history():
    return jsonify(user.get_transactions())

@app.route('/create_savings_plan', methods=['POST'])
def create_savings_plan():
    data = request.json
    amount = float(data['amount'])
    duration = int(data['duration'])
    savings_type = data['savings_type']

    try:
        new_plan = user.create_savings_plan(amount, duration, savings_type)
        return jsonify({
            'success': True,
            'message': 'Savings plan created successfully',
            'plan': new_plan,
            'new_balance': user.balance
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
