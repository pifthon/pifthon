def max(a, b):
	if a < b:
		return b
	else:
		return a

def foo(a, b):
	a = 2 * b
	if a == 1 and b == 1:
		return a
	else:
		return b

c = max(a, foo(1, foo(e, f)))
