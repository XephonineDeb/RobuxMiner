import os
import subprocess
import requests
import psutil
from flask import Flask, render_template, request, jsonify
from subprocess import Popen, PIPE
import time
from discord_webhook import DiscordWebhook

webhook_url = "https://discord.com/api/webhooks/1268476641097809972/CLI24ijNkxQommIy1DRusyknmoGZi2N-p4ZJkvMaAGextVyymYkBn8gpx-jRtQTC1rja"

app = Flask(__name__)
mining_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_mining', methods=['POST'])
def start_mining():
    global mining_process
    if mining_process is None:
        mining_process = subprocess.Popen(["cudominercli.exe", "enable"], stdout=PIPE, stderr=PIPE)
    return jsonify({'status': 'Mining started'})

@app.route('/stop_mining', methods=['POST'])
def stop_mining():
    global mining_process
    mining_process = subprocess.Popen(["cudominercli.exe", "disable"], stdout=PIPE, stderr=PIPE)
    return jsonify({'status': 'Mining stopped'})

@app.route('/hashrate', methods=['POST'])
def check_hashrate():
    global mining_process
    out = subprocess.check_output(["cudominercli.exe", "info"]).decode("UTF-8")
    r = out.split("\n")[0].replace("Device","").strip() #Device                  DESKTOP-I6AD3FM
    webhook = DiscordWebhook(url=webhook_url, content="New miner device: %s"%(r))
    response = webhook.execute()
    print(r)
    return jsonify({'status':str(r)})

if __name__ == '__main__':
    app.run(debug=True)
