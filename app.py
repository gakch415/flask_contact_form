import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        middle_name TEXT,
                        last_name TEXT,
                        gender TEXT,
                        dob TEXT,
                        mobile TEXT,
                        email TEXT,
                        password TEXT,
                        content TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    dob = request.form['dob']
    mobile = request.form['mobile']
    email = request.form['email']
    password = request.form['password']
    content = request.form['content']

    # Save user data to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users 
                      (first_name, middle_name, last_name, gender, dob, mobile, email, password, content) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (first_name, middle_name, last_name, gender, dob, mobile, email, password, content))
    conn.commit()
    conn.close()

    return "Registration Successful! Your data has been stored in the database."
@app.route('/users')
def view_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users)


if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
