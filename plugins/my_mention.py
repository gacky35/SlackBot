from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from . import subMethod

usergroup = subMethod.get_usergroup_list()

@respond_to('@[a-zA-Z0-9]+\s([\s\S]*)')
def reply_to_thread(message, text):
    mention = message.body['text'].split(' ')[0].strip('@')
    for dictionary in usergroup:
        if dictionary['usergroup_name'] == mention:
            mention_dict = dictionary
            break
    sentence = ""
    for member in mention_dict['member']:
        sentence = sentence + "<@" + member + "> "
    sentence = sentence + "\n"
    message.send(sentence, 
            thread_ts=message.thread_ts)

@respond_to('count')
def count_up_reaction(message):
    response = subMethod.get_message(message.body['channel'], 
                                    message.thread_ts)
    data = response['messages'][0]['reactions']
    sorted_data = sorted(data, reverse=True, key=lambda x:x['count'])
    sentence = response['messages'][0]['text'] + '\n\nresult\n'
    for datum in sorted_data:
        sentence = sentence + ":" + datum['name'] + ":" + " "
        for user in datum['users']:
            sentence = sentence + "<@" + user + "> "
        sentence = sentence + "\n"
    message.direct_reply(sentence)

@respond_to('create\s([a-zA-Z0-9]*)\s([a-zA-Z0-9,]*)')
def create_usergroup(message, usergroup_name, member):
    member_list = subMethod.get_member()['members']
    data = {}
    data['usergroup_name'] = usergroup_name
    member_name = member.split(',')
    member_id = []
    for ml in member_list:
        for mn in member_name:
            if ml['name'] == mn or ml['real_name'] == mn:
                member_id.append(ml['id'])
    data['member'] = member_id
    usergroup.append(data)
    subMethod.set_usergroup_list(usergroup)
    message.send('OK')
