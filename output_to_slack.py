import requests
import argparse
import json
from pathlib import Path

TRUFFLEHOG_JSON = 'trufflehog-json'


def prepare_trufflehog_file(webhook, repository):
    trufflehog = []
    if Path(TRUFFLEHOG_JSON).is_file():
        with open(TRUFFLEHOG_JSON, 'r') as file:
            for line in file:
                trufflehog.append(json.loads(line))
        for leak in trufflehog:
            send_to_slack_trufflehog(webhook, leak, repository)
    else:
        print("ERROR: " + TRUFFLEHOG_JSON + " file not found")


def send_to_slack_trufflehog(webhook, leak, repository):
    commit_url = "https://github.com/" + repository + "/commit/" + str(leak['commitHash'])
    payload = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":rotating_light: Potential Secret Discovered! :rotating_light:"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Reason:*\n" + str(leak['reason'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Branch:*\n" + str(leak['branch'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Commit URL:*\n" + commit_url
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Date committed:*\n" + str(leak['date'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Path:*\n" + str(leak['path'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Strings discovered:*\n" + str(leak['stringsFound'])
                        }
                    ]
                }
            ]
    }
    try:
        test1 = requests.post(webhook, json=payload)
        print(test1.content)
    except requests.exceptions.RequestException as e:
        print(e)


parser = argparse.ArgumentParser(argument_default=None, description="Send to Slack")
parser.add_argument('--webhook', type=str, required=True,
                    help='Slack Webhook should go here')
parser.add_argument('--repository', type=str, required=True,
                    help='Repository name. Helps us build the commit hash URL')
args = parser.parse_args()

if args.webhook is None:
    print("Slack Webhook is required!")
    exit()
elif args.webhook:
    prepare_trufflehog_file(args.webhook, args.repository)
