import sqlite3
from flask import Flask, render_template, request, redirect, url_for

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
    try:
        # Debugging: Print form data to terminal
        print("Received Form Data:", request.form)

        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name', '')  # Default to empty if missing
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        password = request.form.get('password')
        content = request.form.get('content', '')

        # Save user data to database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users 
                          (first_name, middle_name, last_name, gender, dob, mobile, email, password, content) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (first_name, middle_name, last_name, gender, dob, mobile, email, password, content))
        conn.commit()
        conn.close()

        print("✅ Data stored successfully in the database.")  # Debug message
        return redirect(url_for('view_users'))  # Redirect to the users list

    except Exception as e:
        print("❌ Error storing data:", e)  # Print error in terminal
        return "An error occurred while storing data."

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
