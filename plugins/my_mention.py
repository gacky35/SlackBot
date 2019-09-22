from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import slack

client_token = 'xoxp-761305137745-754949468914-767736312661-9f26e5c1e6c2282046548a21e303299e'
client = slack.WebClient(token=client_token)
channel_id = 'CND8Z4T3K'

def get_message(client, channel_id, thread_ts):
    response = client.api_call(
            "channels.replies",
            channel = channel_id,
            thread_ts=thread_ts
            )
    return response

@respond_to('@hoge\s.*')
def reply_to_thread(message):
    message.send('<@kayte035> please check it out!', 
            thread_ts=message.thread_ts)

@respond_to('count')
def count_up_reaction(message):
    response = client.channels_replies(
            channel=channel_id, 
            thread_ts=message.thread_ts
            )
    print(response['messages'][0])
