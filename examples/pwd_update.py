def Password_Update(new_pwd, guess_pwd):
	result = False
	if pwd_db == guess_pwd:
		pwd_db = new_pwd
		result = True
	return result

new_pwd = 3
guess_pwd = 5
success = Password_Update(new_pwd, guess_pwd)
