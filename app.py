from flask import Flask, request, render_template
from flask_nav.elements import Navbar, View, Subgroup, Link
from flask_nav import Nav
import src.schemes as schemes

# run with 'flask --app FILENAME run'

app = Flask(__name__)

# help with navigation bar from https://www.geeksforgeeks.org/navigation-bars-in-flask/#
# and https://pythonhosted.org/flask-nav/getting-started.html
nav = Nav()

# View(label/name of page, url/function name, args)
topbar = Navbar('',
                View('Home', 'index'),
                View('One-Time Pad', 'OTP'),
                Subgroup(
                    'Block Ciphers',
                    Link('CBC', 'CBC'),
                    Link('CTR', 'CTR'),
                    Link('OFB', 'OFB'),
                ),
                View('RSA', 'RSA'),
                )

nav.register_element('top', topbar)
nav.init_app(app)


@nav.navigation()
def mynavbar():
    return topbar


@app.route('/')
def index():
    return render_template('index.html', topbar=topbar)


@app.route('/OTP')
def OTP():
    # encryption = None b/c no plaintext or key is in it yet
    return render_template('OTP.html', topbar=topbar, encryption=None)


@app.route('/OTP-encrypt', methods=['POST'])
def OTPEncrypt():

    plaintext = request.form.get('input_text')
    key = request.form.get('key')
    ciphertext = schemes.OTP(plaintext, key)
    # save all data in a dict to keep and display
    encryption = {"plaintext": plaintext, "key": key, "ciphertext": ciphertext}

    return render_template('OTP.html', topbar=topbar, encryption=encryption)


@app.route('/CBC')
def CBC():
    return render_template('CBC.html', topbar=topbar)


@app.route('/CTR')
def CTR():
    return render_template('CTR.html', topbar=topbar)


@app.route('/OFB')
def OFB():
    return render_template('OFB.html', topbar=topbar)


@app.route('/RSA')
def RSA():
    return render_template('RSA.html', topbar=topbar)


if __name__ == '__main__':
    app.run()
