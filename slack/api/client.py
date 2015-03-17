import base64
import json
import logging
import requests

from request import encode_multipart_formdata, encode_urlencode

class Webhook:

    def __init__(self, url, **kwargs):

        self.url = url
        self.proxy = kwargs.get('proxy', None)

        if self.proxy:
            logging.debug("setup webhook to use proxy %s" % self.proxy)

    def send(self, message, **kwargs):

        kwargs['text'] = message
        payload = json.dumps(kwargs)

        params = { 'payload': payload }
        args = encode_urlencode(params)

        if self.proxy:
            args["proxies"] = {"https": self.proxy }

        print args

        rsp = requests.post(self.url, **args)
        body = rsp.text

        return body
        
class OAuth2:

    def __init__(self, access_token, **kwargs):

        self.access_token = access_token

        self.hostname = kwargs.get('hostname', 'slack.com')
        self.endpoint = kwargs.get('endpoint', '/api')
        self.proxy = kwargs.get('proxy', None)
        
        logging.debug("setup API to use %s%s" % (self.hostname, self.endpoint))

        if self.proxy:
            logging.debug("setup API to use proxy %s" % self.proxy)

    def execute_method(self, method, data, encode=encode_urlencode):

        logging.debug("calling %s with args %s" % (method, data))

        data['token'] = self.access_token
        
        url = "https://" + self.hostname + self.endpoint + '/' + method
        logging.debug("calling %s" % url)

        args = encode(data)

        # http://docs.python-requests.org/en/latest/user/advanced/#proxies
        # http://lukasa.co.uk/2013/07/Python_Requests_And_Proxies/

        if self.proxy:
            args["proxies"] = {"https": self.proxy }

        rsp = requests.post(url, **args)
        body = rsp.text

        logging.debug("response is %s" % body)

        try:
            data = json.loads(body)
        except Exception, e:

            logging.error(e)
            logging.debug(body)
            
            error = { 'code': 000, 'message': 'failed to parse JSON', 'details': body }
            data = { 'stat': 'error', 'error': error }

        # check status here...

        return data

    def call (self, method, **kwargs):
        logging.warning("The 'call' method is deprecated. Please use 'execute_method' instead.")
        self.execute_method(method, kwargs)

if __name__ == '__main__':

    import sys
    import pprint
    import time
    import optparse

    parser = optparse.OptionParser(usage="python api.py --access-token <ACCESS TOKEN>")

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
