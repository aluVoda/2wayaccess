from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from Reports import send_reports  
import mysql.connector
from utils.db_utils import connect_to_database
from functools import wraps
from Gates import generate_json

app = Flask(__name__)
app.secret_key = '12345678'  

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'root'

# Login Required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for logging in
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Route to view dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', tables=tables)

# Route to view a specific table
@app.route('/view/<table_name>')
@login_required
def view_table(table_name):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_table.html', table_name=table_name, columns=columns, rows=rows)

# Route to modify (add/update) table data
@app.route('/modify/<table_name>', methods=['GET', 'POST'])
@login_required
def modify_table(table_name):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{v}'" for v in data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        
        try:
            cursor.execute(query)
            conn.commit()
            flash('Data inserted successfully!')
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        return redirect(url_for('view_table', table_name=table_name))
    
    # If it's a GET request, show the form to modify data
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col['Field'] for col in cursor.fetchall()]
    
    return render_template('modify_table.html', table_name=table_name, columns=columns)

# Route to create new tables
@app.route('/create_table', methods=['GET', 'POST'])
@login_required
def create_table():
    if request.method == 'POST':
        table_name = request.form['table_name']
        columns = request.form['columns']  

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            query = f"CREATE TABLE {table_name} ({columns})"
            cursor.execute(query)
            conn.commit()
            flash(f"Table '{table_name}' created successfully!")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        return redirect(url_for('dashboard'))

    return render_template('create_table.html')

# Route to generate reports
@app.route('/generate-reports', methods=['POST'])
@login_required
def generate_reports():
    try:
        send_reports()
        return jsonify({'message': 'Reports generated and sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle access via gates
@app.route('/access', methods=['POST'])
@login_required
def access():
    employee_id = request.form.get('employee_id')
    gate_id = int(request.form.get('gate_id'))
    direction = request.form.get('direction')

    # Generate JSON file for gate access
    generate_json(employee_id, gate_id, direction)
    
    flash('Gate access recorded successfully.')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
