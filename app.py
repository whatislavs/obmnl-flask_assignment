# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        transactions.append({
            'id' : len(transactions)+1,
            'date' : request.form['date'],
            'amount' : float(request.form['amount'])
        })
        return redirect(url_for('get_transactions'))

    return render_template('form.html')

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        for t in transactions:
            if t['id'] == int(transaction_id):
                t['date'] = request.form['date']
                t['amount'] = float(request.form['amount'])
                break
        return redirect(url_for("get_transactions"))
    for t in transactions:
        if t['id'] == int(transaction_id):
            return render_template('edit.html', transaction = t)
    return "Transaction not found"

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for t in transactions:
        if t['id'] == int(transaction_id):
            transactions.remove(t)
            break
    return redirect(url_for("get_transactions"))

@app.route('/search')
def search_transactions():
    if request.args.get('min') and request.args.get('max'):
        try:
            min = float(request.args.get('min'))
            max = float(request.args.get('max'))
            filtered_list = []
            for t in transactions:
                if t['amount'] >= min and t['amount'] <= max:
                    filtered_list.append(t)
            return render_template('transactions.html', transactions = filtered_list)
        except ValueError:
            return "Provide integer values"
    return "Specify min and max"

@app.route('/balance')
def total_balance():
    total_balance = 0
    for t in transactions:
        total_balance += t['amount']
    return "Total balance: " + str(total_balance)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)