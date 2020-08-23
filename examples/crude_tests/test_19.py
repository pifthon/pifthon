def foo(a, b, c):
	if b < 5:
		return list1[0]
	else:
		return c
list1 = [1,2,3]
d = foo(list1[0], 4, ['a', 'b', 'c'])
