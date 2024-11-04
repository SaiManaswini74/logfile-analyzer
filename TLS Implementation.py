import os
import ssl
from flask import Flask, jsonify
from OpenSSL import crypto

# Configuration
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
APP_PORT = 443  # HTTPS default port

def generate_self_signed_cert(cert_file, key_file):
    """Generate a self-signed certificate for TLS."""
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        # Create a key pair
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        # Create a self-signed certificate
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "State"
        cert.get_subject().L = "City"
        cert.get_subject().O = "Organization"
        cert.get_subject().OU = "Organizational Unit"
        cert.get_subject().CN = "localhost"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 year validity
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, "sha256")

        # Write the private key and certificate to files
        with open(cert_file, "wb") as cert_file_obj:
            cert_file_obj.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open(key_file, "wb") as key_file_obj:
            key_file_obj.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

        print("Self-signed certificate created.")
    else:
        print("Certificate and key files already exist.")

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the secure Wisecow app!"})

def main():
    # Generate a self-signed certificate if necessary
    generate_self_signed_cert(CERT_FILE, KEY_FILE)

    # Configure SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Start the Flask application with HTTPS
    app.run(host='0.0.0.0', port=APP_PORT, ssl_context=context)

if __name__ == "__main__":
    main()
