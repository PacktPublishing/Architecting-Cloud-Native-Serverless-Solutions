# Telegram Setup

Inorder to send notifications using Telegram, first you need to create a Telgram bot.  Then you can use the credentials of this bot to talk to the Telegram bot APIs and make it message any users or chats.

## Setup telgram bot and obtain token

Open Telegram on your mobile device, find @BotFather and type
/start. Then follow instructions to create bot and get a token to access the HTTP API.

The botfather will ask a series of question and present you with options.  Ideally the second message your sent to the botfather would be '/newbot'.  This will trigger an interaction where botfather will ask you to chose the bot's anem and username.  At the end of the interaction, botfather will create a bot for you and share the HTTP API token.  This will be a long string - we will save thsi value to the the file `~/.telegram-token` in your home directory.

## Retrieve your chat ID

For a bot to chat with a user, the user has to initiate the chat first.  You can search for your bot from the Telgram app and initiate a conversation.  You will see a start button when you open the chat window and press that.  It will send a bot command "/start".  Once this is doen, we can use the bot API to find the updates / messages that are coming to the bot as below:

The bot API URL starts with `https://api.telegram.org/bot` with the token appended to it.  Then append to that URL the required API method.  Telgram API supports both GET and POST methods.

We will use this to receive chat updates for the boat and retrieve the ID of the user who is chatting with the bot - in this case mine.

```
safeer@serverless102:~$ curl -s "https://api.telegram.org/bot$(cat ~/.telegram-token)/getUpdates"|jq .result[0].message.chat
{
  "id": 1234567890,
  "first_name": "Safeer",
  "type": "private"
}
```

keep this ID for use with the knative app.