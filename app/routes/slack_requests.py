import requests
import os

path = os.environ.get("SLACK_WEB_HOOK")

def sendCardtoSlack(card):
    post_text = f"Card with message {card.message} to board {card.board.title} created"
    request_body = {     
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"New card created! \n*Board name:* {card.board.title}\n *Message:* {card.message} \n {card.likes} :heart:"
                }
            }
        ]
    }
    try:
        response = requests.post(path,json=request_body)
    except Exception as error:
        print("Couldn't post to slack channel")
        print(error.reponse)


