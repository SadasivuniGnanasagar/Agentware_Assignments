from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import math
app = Flask(_name_)
DATABASE_NAME = "loan_management.db"
def setup_database():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS loan_info(
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        principal_amount REAL,
        duration_year INTEGER,
        interest_rate REAL,
        total_due REAL,
        monthly_emi REAL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS payment_records(
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        loan_id INTEGER,
        amount_paid REAL,
        payment_mode TEXT,
        payment_date TEXT)''')

#LEND_ROUTE--
@app.route('/end',methods=['POST'])
def issue_loan():
    info = request.get_json()
    customer = info['customer_id']
    principal = float(info['loan_number'])
    perios = int(info['loan_period'])
    rate = float(info['rate'])

    #interest_calc--
    interest = (principal*rate*period)/100
    total_payable = principal + interest
    montly_installment = math.ceil(total_payable / (period*12))

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO loan_info(customer_id, principal_amount, duration_year, interest_rate, total__due, montly_emi)VALUES(?,?,?,?,?,?)''',
        (customer, principal, period,rate, total_payable, montly_installment))
        generated_loan_id = cursor.lastrowid

    return jsonify({
        'loan_id':generated_loan_id,
        'total_amount':total_payable,
        'monthly_emi':montly_installment})

#LEND_ROUTE----
@app.route('/lend',methods=['POST'])
def issue_loan():
    info = request.get_json()
    customer = info['customer_id']
    principal = float(info['loan_amount'])
    period = int(info['loan_period'])
    rate = float(info['rate'])

    interest = (principal*rate*period)/100
    total_payable = principal + interest
    montly_installment = math.ceil(total_payable/(period*12))

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO loan_info(
        customer_id,principal_amount,duration_year,interest_rate,total_due,montly_emi) VALUES(?,?,?,?,?,?)''',(customer,principal,period,rate,total_payable,montly_installment))
        generated_loan_id = cursor.lastrowid
    return jsonify({
        'loan_id':generated_loan_id,
        'total_amount':total_payable,
        'montly_emi':montly_installment
    })

#PAYMENT_ROUTE---
@app.route('/payment',methods=['POST'])
def record_payment():
    payload = request.get_json()
    loan_ref = payload['loan_id']
    payment_amt = float(payload['amount'])
    method = payload['payment_type']

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO payment_records(loan_id,amount_paid,payment_mode,payment_date) VALUES(?,?,?,?)''',(loan_ref,payment_amt,method,datetime.now().isofromat()))
    reyrn jsonify({'message':'Payment successfully recorded.'})

#LEDGER_MESSAGE---
@app.route('/ledger/int<int:loan_id>',methods=['GET'])
def view_ledger(loan_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        #fetch loan
        cursor.execute('SELECT total_due,montly_emi FROM loan_info WHERE loan_id =?',(loan_id,))
        loan_record = cursor.fetchone()
        if loan_record is none:
            return jsonify({'error':'Loan ID not found'}),404
        total__due,emi_amount = loan_record 

        #fetch all payment for the loan
        cursor.execute('''SELECT amount_paid, payment_mode, payment_date FROM payment_records WHERE loan_id=?''',(loan_id,))payment_logs = cursor.fetchall()
        total_paid = sum([entry[0] for entry in payment_logs])
        remaining_balance = total_paid
        remaining_emis = max(math.ceil(remaining_balance/emi_amount),0)
        return jsonify({
            'loan_id':loan_id,
            'total_amount':total__due,
            'amount_paid':total_paid,
            'remaining_balance':remaining_balance,
            'montly_emi': emi_amount,
            'emi_left':remaining_emis,
            'transactions':[{'amount':p[0],'type':p[1],'date':p[2]} for p in payment_logs]
        })

#ACCOUNT_OVERVIEW---
@app.route('/account/<string:customer_id>',methods=['GET'])
def customer_loans(customer_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT loan_id, principal_amount,total_due,montly_emi FROM loan_info WHERE customer_id = ?''',(customer_id,)) all_loans=cursor.fetchall()
        summary = []
        for loan_id, principal,total,emi in all_loans:
            cursor.execute('SELECT SUM(amount_paid) FROM payment_records WHERE loan_id=?',(loan_id,))
            total_paid = cursor.fetchone()[0]or0
            balance = total-total_paid
            emis_left = max(math.ceil(balamce/emi),0)
            summary.append({
                'loan_id':loan_id,
                'principal':principal,
                'total_amount':total,
                'emi':emi,
                'paid':total_paid,
                'emi_left':emis_left
            })
        return jsonify(summary)

        #SERVER_START--
        if_name_ == '__main__':
            setup_database()
            app.run(debug=True)