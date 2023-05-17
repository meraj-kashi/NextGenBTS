from flask import Flask,render_template,redirect, url_for, request, session
from functools import wraps
import requests
import secrets

login_secret_key = secrets.token_hex(16)

vault_addr='http://0.0.0.0:8200'
vault_token='hvs.kgdsZI7luWko8C7KohLNSK9H'


app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error_message = "Username and password are required."
            return render_template('login.html', error_message=error_message)


        url = f"{vault_addr}/v1/NextGenBTS/userLogin/data/{username}"
        headers = {
        'X-Vault-Token': f"{vault_token}"
        }

        response = requests.request("GET", url, headers=headers)
        response_json = response.json()["data"]
        # Perform user authentication based on form data

        if 'data' in response_json:
            stored_password = response_json['data']['password']

        # Retrieve the stored user credentials from HashiCorp Vault

        if password == stored_password:
            # Authentication successful
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            # Authentication failed
            error_message = "Invalid password."
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    @app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    ip = request.form.get('ip')

    if name and ip:
        item = {'name': name, 'ip': ip}
        collection.insert_one(item)
        return 'Item added successfully'
    else:
        return 'Error: Name and IP are required'

    items = [
        {'name': 'Item 1', 'ip': '192.168.1.1', 'status': 'Active'},
        {'name': 'Item 2', 'ip': '192.168.1.2', 'status': 'Inactive'},
        {'name': 'Item 3', 'ip': '192.168.1.3', 'status': 'Active'}
    ]
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = login_secret_key
    app.run(host='0.0.0.0')