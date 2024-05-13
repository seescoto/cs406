from flask import Flask, request, render_template
from flask_nav.elements import Navbar, View, Subgroup, Link
from flask_nav import Nav
from src import schemes, util

# run with 'flask --app FILENAME run'

app = Flask(__name__)

# help with navigation bar from https://www.geeksforgeeks.org/navigation-bars-in-flask/#
# and https://pythonhosted.org/flask-nav/getting-started.html
nav = Nav()

# View(label/name of page, url/function name, args)
topbar = Navbar('',
                View('Home', 'index'),
                View('One-Time Pad', 'OTP'),
                View('Symmetric Ratchet', 'ratchet'),
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

    # get plaintext & key and store if either is in binary format
    plaintext = request.form.get('input_text')
    key = request.form.get('key')
    binaryPT = request.form.get('binaryPT')
    binaryKey = request.form.get('binaryKey')
    encryption = {}

    # only call funciton if actual values
    if (plaintext and key):
        # find ciphertext w/ OTP() and convert to reg string
        ciphertextBinary = schemes.OTP(
            plaintext, key, binaryPT=binaryPT, binaryKey=binaryKey)
        ciphertextReg = util.binaryStringToString(ciphertextBinary)

        # save all data in a dict to keep and display
        encryption = {"plaintext": plaintext, "key": key,
                      "ciphertextBinary": ciphertextBinary, "ciphertextReg": ciphertextReg}

    return render_template('OTP.html', topbar=topbar, encryption=encryption)


@app.route('/symmetric-ratchet')
def ratchet():
    return render_template('ratchet.html', topbar=topbar, results=None)


@app.route('/sr-activate', methods=['POST'])
def srActivate():
    key = request.form.get('key')
    binaryKey = request.form.get('binaryKey')
    loops = int(request.form.get('loops'))
    results = {}

    if (key):
        s, t = schemes.ratchet(key, loops, binary=binaryKey)
        s = util.intArrayToBinaryString(s)
        t = util.intArrayToBinaryString(t)
        results = {"s": s, "t": t}

    return render_template('ratchet.html', topbar=topbar, results=results)


@app.route('/CBC')
def CBC():
    return render_template('CBC.html', topbar=topbar)


@app.route('/CBC-enc-dec', methods=['POST'])
def CBCEncDec():
    # get plaintext & key and store if either is in binary format
    message = request.form.get('inputText')
    key = request.form.get('key')
    binaryMessage = request.form.get('binaryInput')
    binaryKey = request.form.get('binaryKey')
    encryption = {}

    # only call function if has actual values
    if (message and key):
        # if encrypting
        if request.form.get('submitButton') == "encrypt":
            resultTextBinary = schemes.encryptCBC(
                key, message, binK=binaryKey, binM=binaryMessage)
            resultTextReg = util.binaryStringToString(resultTextBinary)
        # else are decrypting
        else:
            resultTextBinary = schemes.decryptCBC(
                key, message, binK=binaryKey, binC=binaryMessage)
            resultTextReg = util.binaryStringToString(resultTextBinary)

        # save all data in a dict to keep and display
        encryption = {"message": message, "key": key,
                      "resultTextBinary": resultTextBinary, "resultTextReg": resultTextReg}

    return render_template('CBC.html', topbar=topbar, encryption=encryption)


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
