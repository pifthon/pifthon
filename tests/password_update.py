def Password_Update ( new_pwd , guess_pwd ) :
	result = False
	if pwd_db == guess_pwd :
		pwd_db = new_pwd
		result = True
	return downgrade(result,{'A'})

guess_pwd = ' oldpwd '
new_pwd = ' mypwd '
success = Password_Update( new_pwd , guess_pwd )
