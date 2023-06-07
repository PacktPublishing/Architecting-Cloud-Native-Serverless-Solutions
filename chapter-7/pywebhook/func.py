from parliament import Context
import os
import requests
import json

def sendToTelegram(message,chat_id,bot_token):
    url="https://api.telegram.org/bot" + bot_token + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
        }
    headers={ "Content-Type": "application/json" }
    try:
        response = requests.post(url,json=data,headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def main(context: Context):
    """
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    chat_id=os.environ['CHAT_ID']
    bot_token=os.environ['BOT_TOKEN']
    if context['request'].method == "GET":
        return { "message": "Webhook is up" }, 200
    elif context['request'].method == "POST":
        data = context['request'].json
        repo_fullname = data['repository']['full_name']
        url = data['repository']['html_url']
        pusher = data['pusher']['name']
        head_commit_msg = data['head_commit']['message']
        msg = "Git push to <a href=\"" + url + "\">" + repo_fullname + "</a>  |  By <a href=\"https://github.com/" + pusher + "\">" + pusher + "</a>  |  Last commit message: " + head_commit_msg
        msg_status = sendToTelegram(msg, chat_id,bot_token)
        if msg_status == True:
            return { "message": msg }, 200
        else:
            return { "message": "Failed to process the payload" }, 500
    else:
        return { "message": "Method not allowed" }, 405
