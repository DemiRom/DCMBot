import os

from github_webhook import Webhook
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
webhook = Webhook(__name__)

load_dotenv()

ROOT_DIR = os.getenv('ROOT_DIR')

@app.route("/")
def index(): 
    return "<html><h1>Nothing to see here!</h1></html>"

@webhook.hook()
def on_push(data): 
    print("Got push with: {0}".format(data))

    # Stop the bot process
    os.system("systemctl stop dcmbot")
    # Pull latest changes
    os.system(f"git -C {ROOT_DIR} pull origin main")
    # Start the bot process
    os.system("systemctl start dcmbot")

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=80)