def m():
	openA = getbidA()
	openB = getbidB()
	if openA < openB:
		result = openB
	else:
		result = openA

	downgrade(result, result, ['A', 'B'])


def getbidA():
	bidA = 10
	return bidA

def getbidB():
	bidB = 15
	return bidB

m()