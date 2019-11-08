import slack
import pickle
import os

with open('./plugins/client_token.txt') as f:
    client_token = f.read().strip()

client = slack.WebClient(token=client_token)

def get_message(channel_id, thread_ts):
    try:
        response = client.channels_replies(
                channel = channel_id,
                thread_ts=thread_ts
                )
    except:
        response = False
    return response

def get_member():
    return client.users_list()

def get_usergroup_member(usergroup_name):
    usergroup_list = get_usergroup_list()
    member = []
    for ml in usergroup_list:
        if ml['usergroup_name'] == usergroup_name:
            for m in ml['member']:
                member.append(client.users_info(user=m)['user']['name'])
                member.append(client.users_info(user=m)['user']['real_name'])
    return member

def get_usergroup_member_id(usergroup_name):
    usergroup_list = get_usergroup_list()
    member_id = []
    for ml in usergroup_list:
        if ml['usergroup_name'] == usergroup_name:
            member_id.extend(ml['member'])
            break
    return member_id

def get_usergroup_list():
    os.chdir('/data')
    f = open("./usergroup_list.txt", "rb")
    try:
        return pickle.load(f)
    except EOFError:
        return []

def set_usergroup_list(usergroup_list):
    os.chdir('/data')
    f = open("./usergroup_list.txt", "wb")
    pickle.dump(usergroup_list, f)

def username_to_userid(member_list, member_name):
    member_id = []
    for mn in member_name:
        for ml in member_list:
            if ml['name'] == mn or ml['real_name'] == mn:
                member_id.append(ml['id'])
                continue
    return member_id

def userid_to_username(member_list, member_id):
    member_name = []
    for ml in member_list:
        for mi in member_id:
            if ml['id'] == mi:
                member_name.append(ml['profile']['display_name'])
    return member_name

def send_message(channel, text):
    client.chat_postMessage(channel=channel, text=text)
