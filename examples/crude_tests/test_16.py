def max(a, b):
	if a < b:
		return b
	else:
		return a

def foo():
	return a

c = max(a, foo())
'''this
   is
    multiline'''
print(c)