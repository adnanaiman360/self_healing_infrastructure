from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert_receiver():
    data = request.get_json()
    print("Webhook received!")

    if not data or "alerts" not in data:
        return "Invalid alert", 400

    # Loop through all alerts
    for alert in data["alerts"]:
        alertname = alert["labels"].get("alertname", "")
        
        if alertname == "NginxDown":
            print("Alert received: NGINX is down! Attempting restart...")

            os.system("ansible-playbook ../ansible/playbook.yml")

            return "Recovery triggered", 200

    return "No matching alert found", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
   