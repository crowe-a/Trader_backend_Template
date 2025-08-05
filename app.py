from flask import Flask, render_template, redirect, url_for
import threading
from bot import open_browser
from backend import get_ballance
from flask_socketio import SocketIO
app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")
bot_thread = None

# def log_message(msg):
#     """log message"""
#     print(msg)
#     socketio.emit("log", msg)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    global bot_thread
    if open_browser.running:  # Bot zaten çalışıyorsa
        return render_template("start.html", message="Bot has already started .")
    
    bot_thread = threading.Thread(target=open_browser.run)  # Fonksiyon veriyoruz
    bot_thread.start()
    return render_template("start.html", message="Bot started.")

@app.route("/stop")
def stop():
    if open_browser.running:
        open_browser.stop()  # Durdurma fonksiyonu
        return render_template("stop.html", message="Bot stoped.")
    return render_template("stop.html", message="The bot has already stoppedr.")
from flask import jsonify

@app.route("/get_balance")
def get_balance():
    try:
        balance = get_ballance.get_bl()  # Backend işlemi
        return jsonify({"status": "success", "balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0", port=5000)
if __name__ == "__main__":
    app.run(debug=True)
