class config(object):
	SECRET_KEY = "asdfklrnalgasdf"
	FACEBOOK_APP_ID = '1465294083748670'
	FACEBOOK_APP_SECRET = '5e7864ea0eb2ac7b54f43651e3226090'
	debug = False

class Production(config):
	debug = True