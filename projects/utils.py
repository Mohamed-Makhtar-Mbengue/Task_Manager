import requests
import json

def send_slack_notification(message):
    webhook_url = 'https://hooks.slack.com/services/...'  # Remplacez par votre Webhook URL
    payload = {'text': message}
    requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})