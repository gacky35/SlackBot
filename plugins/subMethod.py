import slack

client_token = 'xoxp-761305137745-754949468914-767736312661-9f26e5c1e6c2282046548a21e303299e'
client = slack.WebClient(token=client_token)

def get_message(channel_id, thread_ts):
    response = client.channels_replies(
            channel = channel_id,
            thread_ts=thread_ts
            )
    return response
