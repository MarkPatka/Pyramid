#task palindrome

list2 = list((input('Введите число для проверки: ')))
list1 = list2.copy()

def turn_the_list(list2):
	s = len(list2) - 1
	k = 0
	while s >= k:
		list2[k], list2[s] = list2[s], list2[k]
		s -= 1
		k += 1
	return(list2)

turn_the_list(list2)

if list1 == list2:
	print(f'{list1} is a palindrome!')
else:
	print(f'{list1} is not a palindrome!')