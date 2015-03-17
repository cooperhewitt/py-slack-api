# py-slack-api

There are many wrappers for the Slack API. This one is the Cooper-Hewitt's.

## Example

### OAuth2

	from slack.api.client import OAuth2

	api = OAuth2(ACCESS_TOKEN)

	method = 'chat.postMessage'

	args = {
		'channel': CHANNEL,
		'text': MESSAGE
	}

	rsp = api.execute_method(method, args)
	print rsp

### Webhooks

	from slack.api.client import Webhook

	wh = Webhook(WEBHOOK_URL)
    	wh.send("wub wub wub")

## See also

* https://api.slack.com/
* https://api.slack.com/community#python