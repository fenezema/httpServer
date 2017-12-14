path='/home/lala'

print path
print path[0]
if path[0]=='/':
	print "masuk if"
	path=path.replace(path[0],'',1)
	print path
else:
	print "masuk else"
	print path
