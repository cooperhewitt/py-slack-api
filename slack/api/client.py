import flamework.api.client
import flamework.api.request

class OAuth2(flamework.api.client.OAuth2):

    def __init__(self, access_token, **kwargs):

        
        self.access_token = access_token

        self.hostname = kwargs.get('hostname', 'slack.com')
        self.endpoint = kwargs.get('endpoint', '/api')

        logging.debug("setup API to use %s%s" % (self.hostname, self.endpoint))

if __name__ == '__main__':

    import sys
    import pprint
    import time
    import optparse

    parser = optparse.OptionParser(usage="python api.py --access-token <ACCESS TOKEN>")

    # sudo make me read a config file...

    parser.add_option('--access-token', dest='access_token',
                        help='Your Slack API access token',
                        action='store')

    parser.add_option('--channel', dest='channel',
                        help='The channel you want to send your message to',
                        action='store')

    parser.add_option('--message', dest='message',
                        help='The message you want to send to the channel',
                        action='store')

    parser.add_option("-v", "--verbose", dest="verbose",
                      help="enable chatty logging; default is false", 
                      action="store_true", default=False)

    options, args = parser.parse_args()
    
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    api = OAuth2(options.access_token)

    try:

        method = 'chat.postMessage'

        args = {
            'channel': options.channel,
            'text': options.message
        }

        rsp = api.execute_method(method, args)
        print pprint.pformat(rsp)

    except Exception, e:
        print e

    sys.exit()
