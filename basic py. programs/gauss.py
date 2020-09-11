def main ():
	print("Введите количество уравнений системы: ")
	a = int(input())
	matrix = [[]]
	for row in range(a):
		matrix.append([])
		print("Введите коэффиценты ур-я: ")
		list_num = input().split()
		for el in range(len(list_num)):
			matrix[row].append(int(list_num[el]))

	display_matrix(matrix)
	gauss(matrix)

def display_matrix (matrix):
	for row in range(len(matrix)):
		for col in range(len(matrix[row])):
			print("{:5.2f}".format(matrix[row][col]), end = " ")
			#print(matrix[row][col], end = " ")
		print()
	print("=========")

def check_matrix (matrix, pos):
	if matrix[pos][pos] == 0:
		for row in range(pos + 1, len(matrix) - 1): 
			if matrix[row][pos] != 0:
				matrix[pos], matrix[row] = matrix[row], matrix[pos]
				break
	return matrix[pos][pos] != 0

def modify_matrix (matrix, pos):
	for row in range(pos + 1, len(matrix) - 1):
		k = matrix[row][pos] / matrix[pos][pos]
		for el in range(len(matrix[row])):
			matrix[row][el] -= matrix[pos][el] * k

def gauss (matrix):
	for pos in range(len(matrix) - 1):
		if check_matrix(matrix, pos):
			modify_matrix(matrix, pos)
		display_matrix(matrix)

		
main()


