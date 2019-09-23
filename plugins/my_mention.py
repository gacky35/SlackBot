from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from . import subMethod

@respond_to('@hoge\s.*')
def reply_to_thread(message):
    message.send('<@kayte035> please check it out!', 
            thread_ts=message.thread_ts)

@respond_to('count')
def count_up_reaction(message):
    response = subMethod.get_message(message.thread_ts)
    data = response['messages'][0]['reactions']
    sentence = ""
    for datum in data:
        sentence = sentence + ":" + datum['name'] + ":" + " "
        for user in datum['users']:
            sentence = sentence + "<@" + user + "> "
        sentence = sentence + "\n"
    message.send(sentence, thread_ts=message.thread_ts)
