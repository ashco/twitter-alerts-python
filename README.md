# Twitter Keyword Alert Service
This service sends email alerts when specified Twitter users tweet specific keywords. Twitter is the modern day RRS feed, and this app allows you to monitor for what you want without all the extra noise.

## How to start
Simply run the program with the following command:

`python3 index.py`

## Configuration
### .env

- The following variables must be provided in order to access the Twitter API. Check the Twitter developer docs for info on how to get.

  - TWITTER_CONSUMER_KEY
  - TWITTER_CONSUMER_SECRET
  - TWITTER_ACCESS_TOKEN_KEY
  - TWITTER_ACCESS_TOKEN_SECRET

- The following variables are required in order to set up email sending. Sender email + password are for authentication, recipient is the target email that will receive notifications.

  - SENDER_EMAIL
  - SENDER_EMAIL_PASS
  - RECIPIENT_EMAIL

### config.yaml
Under usernames, provide a key:value pair for each alert configuration you want to watch for. Twitter username is the key, a list of keywords is the value.