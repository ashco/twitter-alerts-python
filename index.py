import os, json, yaml
from emailServer import Email
from tweepy import API, OAuthHandler, Stream, StreamListener
import settings


consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN_KEY')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
recipient_email = os.getenv('RECIPIENT_EMAIL')


with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, config):
        self.config = config

    def _parseData(self, data):
        d = json.loads(data)

        tweetData = {
            'screen_name': d['user']['screen_name'],
            'message': d['text'],
            'urls': list(map(lambda url: url['expanded_url'], d['entities']['urls']))
        }

        return tweetData

    def _sendEmail(self, tweetData):
        subject = f'Twitter Keyword Match: {tweetData["screen_name"]}'
        message = self._composeEmailMessage(tweetData)

        Email().send(recipient_email, subject, message)


    def _composeEmailMessage(self, tweetData):
        message = f'''
New Twitter Keyword Match:

Username: @{tweetData['screen_name']}
Tweet Message: {tweetData["message"]}\n\n'''

        for url in tweetData['urls']:
            message += url + '\n'

        return message

    def on_data(self, data):
        tweetData = self._parseData(data)

        if tweetData['screen_name'] in self.config:
            matchedWords = [keyword for keyword in self.config[tweetData['screen_name']] if keyword in tweetData['message']]

            if len(matchedWords):
                print('Keyword match found!')
                print(tweetData['screen_name'], ':', matchedWords)
                self._sendEmail(tweetData)

        return True

    def on_error(self, status):
        print('ERROR YO!', status)


class TwitterAlerts:
    def __init__(self, config):
        self.config = config
        self.auth = self._createAuth()
        self.api = API(self.auth)
        self.stream = self._createStream(config)

        self.generateInitMsg()

    def generateInitMsg(self):
        maxUsernameLen = len(max(list(self.config.keys()) + ['USERNAME'], key = len))
        print('Twitter keyword alert service initialized')
        print('=========================================')
        print('USERNAME', ' '*(maxUsernameLen - 8), ':', "[KEYWORDS]")
        for username, keywords in self.config.items():
            print(username, ' '*(maxUsernameLen - len(username)), ':', keywords)
        print('')

    def _createAuth(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def getUser(self, username):
        return self.api.get_user(username)

    def _createStream(self, config):
        listener = StdOutListener(config)
        return Stream(self.auth, listener)

    def startFilter(self):
        # convert usernames to ids
        userIds = list(map(lambda username: str(self.getUser(username).id), self.config.keys()))
        # create listener for all userids in config
        self.stream.filter(follow = userIds)


TwitterAlerts(config['usernames']).startFilter()
