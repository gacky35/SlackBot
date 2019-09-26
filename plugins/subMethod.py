import slack
import pickle

client_token = 'xoxp-761305137745-754949468914-767736312661-9f26e5c1e6c2282046548a21e303299e'
client = slack.WebClient(token=client_token)

def get_message(channel_id, thread_ts):
    response = client.channels_replies(
            channel = channel_id,
            thread_ts=thread_ts
            )
    return response

def get_member():
    return client.users_list()

def get_usergroup_list():
    f = open("./plugins/usergroup_list.txt", "rb")
    return pickle.load(f)

def set_usergroup_list(usergroup_list):
    f = open("./plugins/usergroup_list.txt", "wb")
    pickle.dump(usergroup_list, f)

def username_to_userid(member_list, member_name):
    member_id = []
    for ml in member_list:
        for mn in member_name:
            if ml['name'] == mn or ml['real_name'] == mn:
                member_id.append(ml['id'])
    return member_id

def userid_to_username(member_list, member_id):
    member_name = []
    for ml in member_list:
        for mi in member_id:
            if ml['id'] == mi:
                member_name.append(ml['name'])
    return member_name
