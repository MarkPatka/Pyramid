#task1
a = int(input('Укажите количество строк: '))
b = 1
quot_list = []
if a == 0:
	print(' ')
while b <=  a:
	quot_list.append(b * "*")
	b += 1
for i in quot_list:
	print(i)

'''
a = int(input('Укажите количество строк: '))
for x in range(a):
	print('*' * (x+1))
'''


#task2
c = int(input('Укажите число: '))
list1 = range(0, c)
for i in list1:
	if i % 2 == 0:
		print(f'{i} is EVEN')
	else:
		print(f'{i} is ODD')

'''
c = int(input('Укажите число: '))
for x in range (c + 1):
	if x % 2 == 0:
		print(f'{x} is EVEN')
	else:
		print(f'{x} is ODD')
'''



 



