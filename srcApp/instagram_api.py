# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI

loginMain = 'haw22k'
passwordMain = 'Mitra123'


def initialize_api(login=loginMain, password=passwordMain, proxy_name=''):
    api = InstagramAPI(login, password)
    if proxy_name != '':
        api.setProxy(proxy_name)
        # api.setProxy('d0394ffe96:09de558d36@194.28.194.111:52593')
    api.login()
    return api


def get_total_followers_direct_login(login, password, proxy_name=''):

    api = initialize_api(login, password, proxy_name)
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

            #api.s.get('https://www.instagram.com/haw22k/?__a1')
            #api.s.get('https://api.instagram.com/v1/users/search?q=haw2k&access_token=WbnklO47eHmCV2C6rVbzWViVReA6ghx0')

        _ = api.getUserFollowers(api.username_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')


    return len(followers), api.username_id


if __name__ == "__main__":
    followers, username_id = get_total_followers_direct_login("nurtdinov.danil", 'Mitra123', 'd0394ffe96:09de558d36@194.28.194.111:52593')
    print(username_id)
