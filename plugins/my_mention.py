from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from . import subMethod

@listen_to('@[a-zA-Z0-9]+\s([\s\S]*)')
def reply_to_thread(message, text):
    usergroup = subMethod.get_usergroup_list()
    message.body['text'].replace('\n', ' ')
    mention = message.body['text'].split()[0].strip('@')
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
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            message.send(usergroup_name+' is already exist.')
            return
    data = {}
    data['usergroup_name'] = usergroup_name
    member_name = member.split(',')
    member_id = []
    for mn in member_name:
        for ml in member_list:
            if ml['name'] == mn or ml['real_name'] == mn:
                member_id.append(ml['id'])
                continue
        message.send(mn + " is not in this channel")
    data['member'] = member_id
#    data['member'] = subMethod.username_to_userid(member_list, member_name)
    usergroup.append(data)
    subMethod.set_usergroup_list(usergroup)
    message.send('OK')

@respond_to('add\s([a-zA-Z0-9]*)\s([a-zA-Z0-9,]*)')
def add_member(message, usergroup_name, member):
    usergroup = subMethod.get_usergroup_list()
    usergroup_name_list = [usergroup_dict['usergroup_name'] for usergroup_dict in usergroup]
    if usergroup_name not in usergroup_name_list:
        message.send(usergroup_name + " is not exist")
        return
    member_list = subMethod.get_member()['members']
    usergroup_member = subMethod.get_usergroup_member(usergroup_name)
    member_name = member.split(',')
    add_member_name = []
    for mn in member_name:
        if mn not in usergroup_member:
            add_member_name.append(mn)
        else:
            message.send(mn + ' already belongs')
    member_id = []
    ml_id = [ml['id'] for ml in member_list]
    ml_name = [ml['name'] for ml in member_list]
    ml_rname = [ml['real_name'] for ml in member_list]
    for mn in add_member_name:
        if mn in ml_name:
            member_id.append(ml_id[ml_name.index(mn)])
        elif mn in ml_rname:
            member_id.append(ml_id[ml_rname.index(mn)])
        else:
            message.send(mn + " is not in this channel")
    #member_id = subMethod.username_to_userid(member_list, member_name)
    if len(member_id) == 0:
        message.send("No one will add")
        return
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            usergroup_dict['member'].extend(member_id)
            break
    subMethod.set_usergroup_list(usergroup)
    message.send('OK')

@respond_to('delete\s([a-zA-Z0-9]*)\s([a-zA-Z0-9,]*)')
def delete_member(message, usergroup_name, member):
    usergroup = subMethod.get_usergroup_list()
    usergroup_name_list = [usergroup_dict['usergroup_name'] for usergroup_dict in usergroup]
    if usergroup_name not in usergroup_name_list:
        message.send(usergroup_name + " is not exist")
        return
    member_list = subMethod.get_member()['members']
    member_name = member.split(',')
    #member_id = subMethod.username_to_userid(member_list, member_name)
    member_id = []
    ml_id = [ml['id'] for ml in member_list]
    ml_name = [ml['name'] for ml in member_list]
    ml_rname = [ml['real_name'] for ml in member_list]
    for mn in member_name:
        if mn in ml_name:
            member_id.append(ml_id[ml_name.index(mn)])
        elif mn in ml_rname:
            member_id.append(ml_id[ml_rname.index(mn)])
        else:
            message.send(mn + " is not in this channel")
    if len(member_id) == 0:
        message.send("No one will delete")
        return
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            for mi in member_id:
                if mi not in usergroup_dict['member']:
                    message.send(ml_name[ml_id.index(mi)] + " doesn't belong to this")
                else:
                    usergroup_dict['member'].remove(mi)
            break
    subMethod.set_usergroup_list(usergroup)
    message.send('OK. deleted member')

@respond_to('delete_usergroup\s([a-zA-Z0-9]*)')
def delete_usergroup(message, usergroup_name):
    usergroup = subMethod.get_usergroup_list()
    usergroup_name_list = [x['usergroup_name'] for x in usergroup]
    if usergroup_name not in usergroup_name_list:
        message.send(usergroup_name + ' is not exist.')
        return
    new_usergroup = []
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            continue
        new_usergroup.append(usergroup_dict)
    subMethod.set_usergroup_list(new_usergroup)
    message.send('OK. deleted usergroup')

@respond_to('rename\s([a-zA-Z0-9]*)\s([a-zA-Z0-9]*)')
def rename_usergroup(message, usergroup_name, new_usergroup_name):
    usergroups = subMethod.get_usergroup_list()
    usergroup_name_list = [x['usergroup_name'] for x in usergroups]
    if usergroup_name not in usergroup_name_list:
        message.send(usergroup_name + ' is not exist.')
        return
    if new_usergroup_name in usergroup_name_list:
        message.send(new_usergroup_name + ' is exist. so please send another name')
        return
    for usergroup in usergroups:
        if usergroup['usergroup_name'] == usergroup_name:
            usergroup['usergroup_name'] = new_usergroup_name
            break
    subMethod.set_usergroup_list(usergroups)
    message.send('OK. rename usergroup')

@respond_to('list')
def show_usergroup_list(message):
    usergroup = subMethod.get_usergroup_list()
    sentence = ""
    for usergroup_dict in usergroup:
        sentence = sentence + usergroup_dict['usergroup_name'] + "\n"
    message.send(sentence)

@respond_to('show\s([a-zA-Z0-9]*)')
def show_usergroup_member(message, usergroup_name):
    usergroup = subMethod.get_usergroup_list()
    user_list = subMethod.get_member()['members']
    sentence = usergroup_name + " has not created."
    for usergroup_dict in usergroup:
        if usergroup_dict['usergroup_name'] == usergroup_name:
            members = subMethod.userid_to_username(user_list, usergroup_dict['member'])
            sentence = usergroup_name + "\n"
            for member in members:
                sentence = sentence + member + "\n"
            break
    message.send(sentence)

@respond_to('help')
def show_help_message(message):
    message.send('You can use these commands.\n'\
                'You have to mention to @starbot for use these commands.\n'\
                '>>> `create [usergroup_name] [member,member,...]` : create new usergroup.\n'\
                '`add [usergroup_name] [member,member,...]` : add member to exist usergroup.\n'\
                '`delete [usergroup_name] [member,member,...]` : remove member from usergroup.\n'\
                '`delete_usergroup [usergroup_name]` : delete a specified usergroup.\n'\
                '`rename [usergroup_name] [new_usergroup_name]` : change usergroup_name.\n'\
                '`list` : show all usergroup.\n'\
                '`show [usergroup_name]` : show members belonging to a specified usergroup.\n'\
                '`count` : send questionnare\'s result to your DM. this command can only be used on threads. \n')
    
