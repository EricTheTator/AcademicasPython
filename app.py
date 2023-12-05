from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import database  
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        hashed_password = generate_password_hash(password)

        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()
        except mysql.connector.Error as err:
            print("Error: ", err)
            return render_template('register.html', error="An error occurred: " + str(err))
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = database.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            # Password is correct, redirect to dashboard
            return redirect(url_for('dashboard'))
        else:
            # Incorrect password, return error
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    # Here, you'd typically check if the user is logged in
    # If not, redirect them to the login page
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
