from flask import Flask, render_template, jsonify, request

from MY_APP.model.transaction_type import TransactionType
from MY_APP.model.transaction import Transaction, TransactionSchema
from MY_APP.model.income import Income, IncomeSchema
from MY_APP.model.expense import Expense, ExpenseSchema


app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]

incomes =[
    {'description': 'salary', 'amount': 5000}
]

# Homepage route
@app.route('/')
def home():
    return "Welcome to the Homepage. This is a simple Flask application. I'm editing in real time. Help"

# Route to get all incomes
@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)

# Route to add a new income
@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 204

# Route to get all expenses
@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)

# Route to add a new expense
@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204

# Info route that renders the HTML page
@app.route('/info')
def info():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
