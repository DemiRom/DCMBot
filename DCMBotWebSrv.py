import os
import json 
import subprocess

from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

ROOT_DIR = os.getenv('ROOT_DIR')

@app.route("/")
def index(): 
    return "<html><h1>Nothing to see here!</h1></html>"

@app.route("/update", methods = ['GET', 'POST'])
def on_push(): 
    print("Got push")

    # Stop the bot process
    os.system("systemctl stop dcmbot")
    # Pull latest changes
    os.system(f"cd {ROOT_DIR} && git pull origin main")
    # Update the requirements
    os.system(f"/bin/bash -c 'cd {ROOT_DIR} && source .venv/bin/activate && pip3 install -r requirements.txt'")
    # Start the bot process
    os.system("systemctl start dcmbot")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=80)