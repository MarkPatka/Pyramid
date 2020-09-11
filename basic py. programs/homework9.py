#task RSP
import random

items = ['P', 'S', 'R']
restart = 'Y'
winning_combinations = [('R','S'), ('S','P'), ('P','R')]

while restart == 'Y':

	user_choise = input('Paper = P; Scissors = S; Rock = R: ')
	computer_choice = random.choice(items)
	print(f'Computer has chosen {computer_choice}')

	if user_choise not in items:
		print('Incorrect input, try again!')
		continue

	if computer_choice == user_choise:
		print('It`s a draw!')
		restart = input('Would you like to play again? Y_N: ')
	elif (user_choise, computer_choice) in winning_combinations:
		print('You WIN!')
		restart = input('Would you like to play again? Y_N: ')
	else:
		print('You loose!')
		restart = input('Would you like to play again? Y_N: ')

