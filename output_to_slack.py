import requests
import argparse
import json
from pathlib import Path

TRUFFLEHOG_JSON = 'trufflehog-json'


def prepare_trufflehog_file(webhook):
    trufflehog = []
    if Path(TRUFFLEHOG_JSON).is_file():
        with open(TRUFFLEHOG_JSON, 'r') as file:
            for line in file:
                trufflehog.append(json.loads(line))
        for leak in trufflehog:
            send_to_slack_trufflehog(webhook, leak)


def send_to_slack_trufflehog(webhook, leak):
    payload = {
        "attachments": [
            {
                "fallback": ":rotating_light: truffleHog finding! :rotating_light:",
                "pretext": ":rotating_light: truffleHog finding! :rotating_light:"},
                {"title": "Reason: ", "text": str(leak['reason']), "color": "#ff0000"},
                {"title": "Branch: ", "text": str(leak['branch']), "color": "#ff0000"},
                {"title": "Commit hash: ", "text": str(leak['commitHash']), "color": "#ff0000"},
                {"title": "Date committed: ", "text": str(leak['date']), "color": "#ff0000"},
                {"title": "Path: ", "text": str(leak['path']), "color": "#ff0000"},
                {"title": "Strings found: ", "text": str(leak['stringsFound']), "color": "#ff0000"}
        ]
    }
    try:
        requests.post(webhook, json=payload)
    except requests.exceptions.RequestException as e:
        print(e)


parser = argparse.ArgumentParser(argument_default=None, description="Send to Slack")
parser.add_argument('--webhook', type=str, required=True,
                    help='Slack Webhook should go here')
args = parser.parse_args()

if args.webhook is None:
    print("Slack Webhook is required!")
    exit()
elif args.webhook:
    prepare_trufflehog_file(args.webhook)
