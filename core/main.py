from flask import Flask,render_template,redirect, url_for, request
import requests

vault_addr='http://0.0.0.0:8200'
vault_token='hvs.kgdsZI7luWko8C7KohLNSK9H'


app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

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
            # ... Add your user login logic here ...
            print("hereeeeeee")
            return redirect(url_for('home'))
        else:
            # Authentication failed
            # ... Handle authentication failure ...
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')