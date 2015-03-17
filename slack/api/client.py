import urllib
import httplib
import base64
import json
import logging
from urlparse import urlparse

from request import encode_multipart_formdata, encode_urlencode

class Webhook:

    def __init__(self, url):
        self.url = url

    def send(self, message, **kwargs):
        
        kwargs['text'] = message
        payload = json.dumps(kwargs)

        params = { 'payload': payload }
        (headers, body) = encode_urlencode(params)

        info = urlparse(self.url)

        conn = httplib.HTTPSConnection(info.netloc)
        conn.request('POST', info.path, body, headers)

        rsp = conn.getresponse()
        body = rsp.read()

        return body

class OAuth2:

    def __init__(self, access_token, **kwargs):

        self.access_token = access_token

        self.hostname = kwargs.get('hostname', 'slack.com')
        self.endpoint = kwargs.get('endpoint', '/api')

        logging.debug("setup API to use %s%s" % (self.hostname, self.endpoint))

    def execute_method(self, method, kwargs, encode=encode_urlencode):

        logging.debug("calling %s with args %s" % (method, kwargs))

        kwargs['method'] = method
        kwargs['token'] = self.access_token

        (headers, body) = encode(kwargs)

        url = self.endpoint + '/' + method
        logging.debug("calling %s" % url)

        conn = httplib.HTTPSConnection(self.hostname)
        conn.request('POST', url, body, headers)

        rsp = conn.getresponse()
        body = rsp.read()

        logging.debug("response is %s" % body)

        try:
            data = json.loads(body)
        except Exception, e:
            logging.error(e)
            raise Exception, e

        # check status here...

        return data

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
    
    sys.exit()

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
