import os
import json
from tweepy import OAuthHandler, Stream, StreamListener

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')


config = {
    # WirecutterDeals
    '3255034008': {
        'keywords': ['iphone', 'tripod'],
        'messageTemplate': "This is the message template"
    },
    # AKC_DEV
    '2409114414': {
        'keywords': ['python', 'javascript'],
        'messageTemplate': "Wasup boi"
    }
}


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, config):
        self.config = config

    def _parseData(self, data):
        d = json.loads(data)

        screen_name = d['user']['screen_name']
        id = str(d['user']['id'])
        text = d['text']
        urls = list(map(lambda url: url['expanded_url'], d['entities']['urls']))

        return (screen_name, id, text, urls)

    def sendEmail(self, screen_name, id, text, urls):
        print('Username: {0}\nID: {1}\nMessage: {2}\nURLs: {3}'.format(screen_name, id, text, urls), end='\n\n')

    def composeEmailMessage(self):
        pass

    def on_data(self, data):
        screen_name, id, text, urls = self._parseData(data)

        # check for keyword match
        textSet = set(text.lower().split(' '))
        keywordSet = set(self.config[id]['keywords'])
        # # # overlap in words

        if len(textSet & keywordSet):
            self.sendEmail(screen_name, id, text, urls)

        # print(data, end="\n")
        return True

    def on_error(self, status):
        print(status)


class Server:
    def __init__(self, config):
        # self.config = config
        self.stream = self._createStream(config)

        print('Twitter keyword alert service initialized.')
        # create listener for all userids in config
        self.stream.filter(follow = config.keys())
        # self.stream.filter(track=['baseball'])


    def _createStream(self, config):
        listener = StdOutListener(config)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return Stream(auth, listener)



    def composeEmailMessage(self):
        pass

    def sendEmail(self):
        pass



server = Server(config)