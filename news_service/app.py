from pynytimes import NYTAPI
import time
from flask import Flask, render_template, request, redirect, url_for, session,flash
import requests
import os

nyt = NYTAPI("UsLI71E1Rg7Q6qdcmNP9dJ6wouJMvNFl", parse_dates=True)
import requests






done  = False
cpt = 0
while (not done ):
    try :
        response  = requests.get('http://mysql-flask-service:5000/' ).text 
        if (response == "ready"):
            done = True
    except :
        time.sleep(1)
        cpt  = cpt + 1
        if (cpt == 5):
            done = True
            


app = Flask(__name__)
app.secret_key = 'super secret key'
# http://mysql-flask-service:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        form = {"username" : request.form['username'] , "password": request.form['password']}
        # Check if account exists using request
        response  = requests.post('http://mysql-flask-service:5000/login'  , form)
        response = response.json()

        
                # If account exists in accounts table in out database
        if response[0] == "good":
            # Create session data, we can access this data in other routes
            account = response[1]
            global session
            session = {
                'loggedin'  : True,
                'username' : account['username'],
                'account' : account
            }
            # Redirect to home page
            return redirect("/home")
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")



# http://mysql-flask-service:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        form = {"username" : request.form['username'] ,"email" : request.form['email'] , "password": request.form['password']}
        # Check if account exists using request
        response  = requests.post('http://mysql-flask-service:5000/register'  , form)
        response = response.text
        
        # If account exists show error and validation checks
        if response != "You have successfully registered!" : 
            flash(response, "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            flash(response, "success")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")

# http://mysql-flask-service:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users
  


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if not('loggedin' in session):
        # User is not loggedin show them the home page
        return redirect(url_for('login'))
    return render_template('auth/profile.html', account=session['account'],title="Profile")  

def give_article_images_and_names(results):
    for result in results :
        try : 
            
            if not("multimedia" in result):
                url_dict = result['media'][0]['media-metadata'][2]
            else :
                url_dict = result['multimedia'][0]
            if ( "static01.nyt.com" not in  url_dict['url'] ):
                result['image_url'] = 'https://static01.nyt.com/' + url_dict['url']
            else :
                result['image_url'] =  url_dict['url']

        except:
            if ("book_image" in result):
                result['image_url'] = result['book_image']
                try :
                    result['url'] = result['buy_links'][0]['url']
                except:
                    result['url'] = ""
             
            else :
                result['image_url'] =  'https://upload.wikimedia.org/wikipedia/commons/4/49/A_black_image.jpg' 

        try :
            if ("title" in result):
                result['main_headline']  = result['title'] 
            else : 
                result['main_headline']= result['headline']['main'] 
            if (result['main_headline'] is None):
                result['main_headline']=''
        except : 
            result['main_headline'] = ''
    return results

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if not('loggedin' in session):
        # User is not loggedin show them the home page
        return redirect(url_for('login'))  
    """
    if request.method == 'POST':
        form = {"query" : request.form['query']}"""
    # User loggedin redirect to login page
    top_stories = nyt.top_stories()
    top_stories = give_article_images_and_names(top_stories)
    most_viewed = nyt.most_viewed(days=7)
    most_viewed = give_article_images_and_names(most_viewed)
    most_shared = nyt.most_shared(days=7)
    most_shared = give_article_images_and_names(most_shared)
    best_sellers= nyt.best_sellers_list()
    best_sellers = give_article_images_and_names(best_sellers)

    return render_template('home.html' , top_stories  = top_stories,
                           most_viewed = most_viewed,most_shared = most_shared,
                           best_sellers = best_sellers)

@app.route('/search' , methods=['GET', 'POST'])
def search_page():
    # Check if user is loggedin
    if not('loggedin' in session):
        # User is not loggedin show them the home page
        return redirect(url_for('login')) 
    if request.method == 'POST' and 'text_query' in request.form:
        query = request.form["text_query"]
    else : 
        query = " " 
    search_result =  nyt.article_search(
    query = query, # Search for articles about Obama
    results = 30)
    search_result = give_article_images_and_names(search_result)
    return render_template('search_page.html' , search_result = search_result , search_query = query)

'''@app.route('/searched')
def search_page():
'''

@app.route('/logout')
def log_out():
    global session
    session = None
    return redirect(url_for('login'))  
    #return nyt.most_viewed(days=7)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5500))
    app.run(debug=True,  port=port)

# Sign up
# Login
# search
# show search history
# page de most # page de search # page de article