# py-slack-api

There are many wrappers for the Slack API. This one is the Cooper-Hewitt's.

## Example

	from slack.api.client import OAuth2

	api = OAuth2(ACCESS_TOKEN)

	method = 'chat.postMessage'

	args = {
		'channel': CHANNEL,
		'text': MESSAGE
	}

	rsp = api.execute_method(method, args)
	print rsp

## TO DO

* Use [py-flamework-api](https://github.com/cooperhewitt/py-flamework-api) as a base class

## See also

* https://api.slack.com/
* https://api.slack.com/community#python