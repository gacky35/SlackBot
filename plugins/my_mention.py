from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from . import subMethod

@listen_to('@[a-zA-Z0-9]+\s([\s\S]*)')
def reply_to_thread(message, text):
    usergroup = subMethod.get_usergroup_list()
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
    usergroup = subMethod.get_usergroup_list()
    member_list = subMethod.get_member()['members']
    data = {}
    data['usergroup_name'] = usergroup_name
    member_name = member.split(',')
    data['member'] = subMethod.username_to_userid(member_list, member_name)
    usergroup.append(data)
    subMethod.set_usergroup_list(usergroup)
    message.send('OK')

@respond_to('add\s([a-zA-Z0-9]*)\s([a-zA-Z0-9,]*)')
def add_member(message, usergroup_name, member):
    usergroup = subMethod.get_usergroup_list()
    member_list = subMethod.get_member()['members']
    member_name = member.split(',')
    member_id = subMethod.username_to_userid(member_list, member_name)
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            usergroup_dict['member'].extend(member_id)
            break
    subMethod.set_usergroup_list(usergroup)
    message.send('OK')

@respond_to('delete\s([a-zA-Z0-9]*)\s([a-zA-Z0-9,]*)')
def delete_member(message, usergroup_name, member):
    usergroup = subMethod.get_usergroup_list()
    member_list = subMethod.get_member()['members']
    member_name = member.split(',')
    member_id = subMethod.username_to_userid(member_list, member_name)
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            for mi in member_id:
                usergroup_dict['member'].remove(mi)
            break
    subMethod.set_usergroup_list(usergroup)
    message.send('OK. deleted member')

@respond_to('delete_usergroup\s([a-zA-Z0-9]*)')
def delete_usergroup(message, usergroup_name):
    usergroup = subMethod.get_usergroup_list()
    new_usergroup = []
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            continue
        new_usergroup.append(usergroup_dict)
    subMethod.set_usergroup_list(new_usergroup)
    message.send('OK. deleted usergroup')
