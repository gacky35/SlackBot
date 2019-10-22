with open('./access_token.txt') as f:
    API_TOKEN = f.read().strip()

DEFAULT_REPLY = "Can't do that! Please try `@starbot help`"

PLUGINS = ['plugins']
