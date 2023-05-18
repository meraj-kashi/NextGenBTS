from flask import Flask,render_template,redirect, url_for, request, session
from functools import wraps
import requests
import secrets
import subprocess
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

# Load config from file
with open('config.json') as config_file:
    config = json.load(config_file)

login_secret_key = secrets.token_hex(16)

vault_addr=f"http://{config['secret']['host']}:{config['secret']['port']}"
vault_token=config['secret']['token']

client = MongoClient(f"mongodb://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}")
db = client[config['database']['name']]
collection = db[config['database']['collection']]


app = Flask(__name__)

def ip_status(ip):
    if ip:
        try:
            result = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return 0
            else:
                return 1
        except subprocess.TimeoutExpired:
            return 1
        except subprocess.CalledProcessError as e:
            return 1

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

@app.route('/home', methods=['GET'])
@login_required
def home():
    items = collection.find()

    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.json.get('name')
    ip = request.json.get('ip')

    if name and ip:
        if ip_status(ip) == 0:
            connectivity = "connected"
        else:
            connectivity = "disconnected"

        item = {'name': name, 'ip': ip, 'connectivity': connectivity}
        collection.insert_one(item)

        response_item = {'connectivity': connectivity, 'message': f'{name} BTS added successfully'}

        return response_item
    else:
        return {'message': 'BTS ID and IP are required'}

@app.route('/remove', methods=['POST'])
def remove_item():
    item_id = request.json.get('id')

    if item_id:
        document = collection.find_one({'_id': ObjectId(item_id)})
        name = document['name']

        result = collection.delete_one({'_id': ObjectId(item_id)})

        if result.deleted_count > 0:
            return {'message': f'{name} BTS removed successfully'}
        else:
            return {'error': 'BTS not found'}, 404
    else:
        return {'error': 'Invalid request'}, 400


if __name__ == '__main__':
    app.config['SECRET_KEY'] = login_secret_key
    app.run(host='0.0.0.0')