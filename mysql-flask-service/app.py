import mysql.connector
import time
from flask import Flask, render_template, request, redirect, url_for, session,flash
import re
done  = False
while (not done ):
    try :
        connection = mysql.connector.connect(
    user ='root', password='root', host='mysql', port="3306", database="db" )
        done = True
    except : 
        time.sleep(1)


app = Flask(__name__)
app.secret_key = 'super secret key'
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests

@app.route("/")
def ready():
    if done:
        return 'ready'
    else:
        return 'not ready'

@app.route('/login', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            return ["good", account]
        else:
            # Account doesnt exist or username/password incorrect
            return ['bad']
    return [""]



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = connection.cursor(dictionary=True)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s", [username] )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            return "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return "Invalid email address!"
        elif not re.match(r'[A-Za-z0-9]+', username):
            return "Username must contain only characters and numbers!"
        elif not username or not password or not email:
            return "Incorrect username/password!"
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES ( %s, %s, %s)', (username,email, password))
            connection.commit()
            return "You have successfully registered!"
        
    elif request.method == 'POST':
        return "not_filled"
    # Show registration form with message (if any)
    return  ""

# http://localhost:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users
 




if __name__ =='__main__':
	app.run(Debug=True)







'''def authenticate( client_name, client_pass):

def register(client_name, client_pass):

def add_or_remove_like (client_name, article_url):

def add_or_remove_hate (client_name, article_url):

def add_to_history (client_name, article_url):

def remove_from_history (client_name , article_url):

def delete_client ( client_name):'''
