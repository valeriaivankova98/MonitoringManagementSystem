import database


USER_ID = 1

database.check_user(USER_ID)
database.set_token(USER_ID, 'token123')
database.set_folder(USER_ID, 'folder_id')
print(database.get_user_data(USER_ID))
database.clear_user(USER_ID)
user_data = database.get_user_data(USER_ID)
print(user_data is None or not user_data['token'])

