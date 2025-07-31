from flask import Flask, render_template, redirect, url_for
import threading
from bot import open_browser  # bot  open_browser import

app = Flask(__name__)

bot_thread = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    global bot_thread
    if open_browser.running:  # is it runnig?
        return "Bot still working."
    
    bot_thread = threading.Thread(target=open_browser.run)  # parantezsiz
    bot_thread.start()  # start thread 
    return redirect(url_for("index"))

@app.route("/stop")
def stop():
    if open_browser.running:
        open_browser.stop()  # stop bot 
        return redirect(url_for("index"))
    return "Bot stoped."

if __name__ == "__main__":
    app.run(debug=True)
