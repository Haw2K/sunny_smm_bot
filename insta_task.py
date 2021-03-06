#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.userinfo import UserInfo
from srcApp import sql_works
from srcApp import instagram_api
from datetime import datetime
import os

#initialize variables
#threading_errors = []

def post_processing(insta_front_tasks,ignore_processing = 0):

    insta_tasks = []

    if ignore_processing == 0:

        ui = UserInfo()
        users_id = []
        error_message = ''
        insta_front_tasks = list(insta_front_tasks)
        subscribers_exept = 0

        # only unique logins
        logins_list = []
        for task_values in reversed(insta_front_tasks):
            find_login = task_values[5] in logins_list
            if find_login == False:
                logins_list.append(task_values[5])
            else:
                insta_tasks.append([task_values[0], task_values[4], task_values[1], task_values[2], datetime.now(), 0,
                                    'Not unique login', task_values[5], task_values[6], task_values[3],0])
                insta_front_tasks.remove(task_values)

        # for task_values in reversed(insta_front_tasks):
        #     try:
        #         user_id = ui.get_user_id_by_login(task_values[5])
        #         users_id.append(user_id)
        #     except Exception:
        #
        #         insta_tasks.append([task_values[0], task_values[4], task_values[1], task_values[2], datetime.now(), 0,
        #                             'Except get instagram user_id', task_values[5], task_values[6], task_values[3]])
        #         insta_front_tasks.remove(task_values)

        followers_quantities = []
        users_ids = []
        for task_values in reversed(insta_front_tasks):
            try:
                #user_id = ui.get_user_id_by_login(task_values[5])
                followers_len, users_id = instagram_api.get_total_followers_direct_login(task_values[5],task_values[6])
                followers_quantities.append(followers_len)
                users_ids.append(users_id)
            except Exception:

                insta_tasks.append([task_values[0], task_values[4], task_values[1], task_values[2], datetime.now(), 0,
                                    'Except get followers_quantities', task_values[5], task_values[6], task_values[3],0])
                insta_front_tasks.remove(task_values)


        followers_quantities = followers_quantities[::-1]
        users_ids = users_ids[::-1]


        # try:
        #     followers_quantities = instagram_api.get_total_followers(reversed(users_id))
        # except Exception:
        #     error_message = 'Except get followers_quantities'
        #     subscribers_exept = 1

        for task_values in insta_front_tasks:

            index = insta_front_tasks.index(task_values)
            subscribers_now = 0
            users_id = ''
            if followers_quantities.__len__() > 0:
                subscribers_now = followers_quantities[index]
                users_id = users_ids[index]

            #subscribers_now = 0
            insta_tasks.append([task_values[0], task_values[4], task_values[1], task_values[2], datetime.now(),
                                subscribers_now, error_message, task_values[5], task_values[6], task_values[3], users_id])
    else:
        #ignore processing loop
        for task_values in insta_front_tasks:
            insta_tasks.append(
                [task_values[0], task_values[4], task_values[1], task_values[2], datetime.now(), 0,
                 '', task_values[5], task_values[6], task_values[3],0])

    return insta_tasks

def insta_bot_start(task):
    print(task)
    #task: task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id
    arg_task = task[:]
    arg_task[8] = arg_task[8].replace(', ', ':')
    if arg_task[1] != None:
        arg_task[1] = arg_task[1].timestamp()
    if arg_task[2] != None:
        arg_task[2] = arg_task[2].timestamp()

    str_task = ' '.join(str(v) for v in arg_task)

    #p = subprocess.Popen([sys.executable, "python3.5 instabot_example.py %s" % str_task],
    #                     stdout=subprocess.PIPE,
    #                     stderr=subprocess.STDOUT)

    os.system("python3.5 instabot_example.py %s &" % str_task)



if __name__ == "__main__":

    #only active instagram tasks from frontend
    #return: task_id, account_id, type_id, tags, user_id, login, password
    insta_front_tasks = sql_works.get_tasks_front()

    #returns: task_id, user_id, account_id, type_id, date_start, subscribers_now, error_message, login, password, tags
    insta_tasks = post_processing(insta_front_tasks)
    #insta_tasks = post_processing(insta_front_tasks,1)

    #check not started tasks
    #returns:  task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id, error_text, user_id
    insta_backend_tasks = sql_works.task_manager(insta_tasks)

    sql_works.return_statictic_to_front(insta_backend_tasks)

    #threads = []
    #with ThreadPoolExecutor(max_workers=2) as executor:
    count_bot_examples = 0
    for task in insta_backend_tasks:
        #new and restart
        if task[5] == 0 or task[5] == 1:
            if count_bot_examples < 4:
                count_bot_examples = count_bot_examples + 1
            #executor.submit(insta_bot_start, task)
                insta_bot_start(task)
            #t = threading.Thread(target=insta_bot_start, args=(task,))
            #threads.append(t)
            #t.start()


    # args = [argumentsA, argumentsB, argumentsC]
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     for arg in args:
    #         executor.submit(call_script, arg)
    #print('All tasks has been finished')


    # for task in insta_backend_tasks:
    #     #new and restart
    #     if task[5] == 0 or task[5] == 1:
    #        # insta_bot_start(task)
    #         t = threading.Thread(target=insta_bot_start, args=(task,))
    #         threads.append(t)
    #         t.start()
    #
    #
    #
    #
    #
#    for t in threads:
 #       t.join()




