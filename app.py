from flask import request,render_template,Flask
import socket

app = Flask(__name__)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"IP:{ip_address}")

@app.route("/")
def hello_world():
    return render_template("qrcode.html")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5432)