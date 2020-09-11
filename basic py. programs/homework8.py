#task guess number
import random

number = random.randint(1, 50)
tries = 6
user_number = int(input(f'Try to guess number from 1 to 50.\n You have left {tries} tries: '))
while tries > 1:
	print(user_number)
	if user_number == number:
		print(f'Congratulations! The number was {number}')
		break
	elif user_number > number:
		print('The right number is less\n')
		tries -= 1
		user_number = int(input(f'Try to guess number from 1 to 50.\n You have left {tries} tries: '))		
	else:
		print('The right number is greater\n')
		tries -= 1
		user_number = int(input(f'Try to guess number from 1 to 50.\n You have left {tries} tries: '))		
print('Game over')

