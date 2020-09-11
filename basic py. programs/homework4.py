
#task1
a = int(input('Введите ваше число: '))
list1 = range(0, a + 1)
list2 = []
for x in list1:
	if x % 3 == 0 or x % 5 == 0:
		list2.append(x)
sumofel = 0
for i in list2:
	sumofel = sumofel + i
print(sumofel)	

'''
a = int(input('Введите ваше число: '))
total sum = 0
for x in range(a + 1):
	if x % 3 == 0 or x % 5 == 0:
		total_sum += x
'''

#task2
first_list = list(input("Введите числа первого списка: ").split())
second_list = list(input("Введите числа второго списка: ").split())
joined_list = []
for i in first_list:
	if int(i) % 2 != 0:
		joined_list.append(i)
for l in second_list:
	if int(l) % 2 == 0:
		joined_list.append(l)
print(joined_list)

'''

'''
