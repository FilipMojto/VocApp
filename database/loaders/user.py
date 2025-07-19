# __ALL__ = ['load_users_json']

# import json
# import sqlite3

# from typing import List
# import os, sys

# # Ensure the path to the seeds directory is in the system path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

# from shared.vocapptypes import User

# def load_users_json() -> List[User]:
#     SEEDER_FILE_PATH = './seeds/users.json'
    
#     with open(SEEDER_FILE_PATH, 'r', encoding='utf-8') as file:
#         users_data = json.load(file)

#     users: List[User] = []

#     for user in users_data.get('users', []):
#         user_obj = User(
#             id=user.get('id'),
#             username=user['name'],
#             password=user['password']
#         )
#         users.append(user_obj)

#     return users
