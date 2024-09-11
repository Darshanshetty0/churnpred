# app.py
import pymysql 
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, url_for, request
import pickle
import pandas as pd

app = Flask(__name__)

host_name = "127.0.0.1"
user_name = "root"
user_password = "darshan253"
db_name = "CustomerDB"

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection(host_name, user_name, user_password, db_name)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('customer_info.html')

@app.route('/customer_info', methods=['POST'])
def customer_info():
    if request.method == 'POST':
        cursor = connection.cursor()
        table = 'CustomerInfo'
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        results = cursor.fetchall()
        tr = len(results[0])
        cursor.close()
    return render_template('customer_info.html', result=results, table=table, tr = tr)

@app.route('/customer_insight', methods=['POST'])
def customer_insight():
    if request.method == 'POST':
        cursor = connection.cursor()
        table= request.form.get('table')  # Get the table name from the dropdown
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        results = cursor.fetchall()
        tr = len(results[0])
        cursor.close()
    return render_template('customer_info.html', result=results, table=table, tr = tr)

@app.route('/churn_prediction', methods=['POST'])
def churn_prediction():
    return render_template('churn_prediction.html', result = None)

@app.route('/churn_prediction_predict', methods=['POST'])    
def churn_prediction_predict():
        customer_age = int(request.form.get('customer_age'))
        gender = int(request.form.get('gender'))
        dependent_count = int(request.form.get('dependent_count'))
        education_level = int(request.form.get('education_level'))
        marital_status = int(request.form.get('marital_status'))
        income_category = int(request.form.get('income_category'))
        card_category = int(request.form.get('card_category'))
        months_on_book = int(request.form.get('months_on_book'))
        total_relationship_count = int(request.form.get('total_relationship_count'))
        months_inactive_12_mon = int(request.form.get('months_inactive_12_mon'))
        contacts_count_12_mon = int(request.form.get('contacts_count_12_mon'))
        credit_limit = float(request.form.get('credit_limit'))
        total_revolving_bal = int(request.form.get('total_revolving_bal'))
        avg_open_to_buy = float(request.form.get('avg_open_to_buy'))
        total_amt_chng_q4_q1 = float(request.form.get('total_amt_chng_q4_q1'))
        total_trans_amt = int(request.form.get('total_trans_amt'))
        total_trans_ct = int(request.form.get('total_trans_ct'))
        total_ct_chng_q4_q1 = float(request.form.get('total_ct_chng_q4_q1'))
        avg_utilization_ratio = float(request.form.get('avg_utilization_ratio'))
        
        input_data = pd.DataFrame({
            'Customer_Age': [customer_age],
            'Gender': [gender],
            'Dependent_count': [dependent_count],
            'Education_Level': [education_level],
            'Marital_Status': [marital_status],
            'Income_Category': [income_category],
            'Card_Category': [card_category],
            'Months_on_book': [months_on_book],
            'Total_Relationship_Count': [total_relationship_count],
            'Months_Inactive_12_mon': [months_inactive_12_mon],
            'Contacts_Count_12_mon': [contacts_count_12_mon],
            'Credit_Limit': [credit_limit],
            'Total_Revolving_Bal': [total_revolving_bal],
            'Avg_Open_To_Buy': [avg_open_to_buy],
            'Total_Amt_Chng_Q4_Q1': [total_amt_chng_q4_q1],
            'Total_Trans_Amt': [total_trans_amt],
            'Total_Trans_Ct': [total_trans_ct],
            'Total_Ct_Chng_Q4_Q1': [total_ct_chng_q4_q1],
            'Avg_Utilization_Ratio': [avg_utilization_ratio]
        })
    
        with open('./models/churn_model.pkl', 'rb') as f:
            loaded_model = pickle.load(f)
        result= loaded_model.predict(input_data)
        return render_template('churn_prediction.html', result = result)

@app.route('/customer_update')
def customer_update():
    return render_template('customer_update.html')

@app.route('/retrieve', methods=['POST'])
def retrieve():
    try:
        if request.method == 'POST':
            cursor = connection.cursor()
            table = str(request.form['table'])  # Get the table name from the dropdown
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return render_template('index.html', result=results)
    except pymysql.MySQLError as e:
        error_msg = f"Database error: {e}"
        print(error_msg)
        return render_template('index.html', result=error_msg)
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        return render_template('index.html', result=error_msg)


if __name__ == '__main__':
    app.run(debug=True)
