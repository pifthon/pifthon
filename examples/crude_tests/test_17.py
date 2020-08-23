def max(a, b):
	if a < b:
		return b
	else:
		return a

def foo():
	b = a/2

	if b > a:
		return a
	else:
		return foo()

c = foo()

