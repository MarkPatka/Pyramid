#task1
import random

cards1 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
hand = []
while len(hand) <= 5:
	a = random.choice(cards1)
	hand.append(a)
print(hand)

a = cards1[:5]
b = cards1[5:-5]
c = cards1[-5:]

a_list = []
for i in hand:
	for j in a:
		if i == j:
			a_list.append(i)

b_list = []
for i in hand:
	for j in b:
		if i == j:
			b_list.append(i)

c_list = []
for i in hand:
	for j in c:
		if i == j:
			c_list.append(i)

res = (len(c_list) * -1) + (len(b_list) * 0) + (len(a_list) * 1)

print(res)

