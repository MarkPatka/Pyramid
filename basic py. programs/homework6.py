import random

card_lears = ['H', 'S', 'D', 'C']
card_strength = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
table_cards = []
hand_cards = []
cards = []

for i in card_lears:
	for j in card_strength:
		card = i + j
		cards.append(card)

while len(table_cards) <= 4:
	t = random.choice(cards)
	if t in table_cards:
		continue
	table_cards.append(t)
print(table_cards)

while len(hand_cards) <= 1:
	k = random.choice(cards)
	if k in hand_cards:
		continue
	if k in table_cards:
		continue
	hand_cards.append(k)
print(hand_cards)

played_cards = hand_cards + table_cards
all_lears = []
for i in played_cards:
	l = i[0]
	all_lears.append(l)

dict1 = {}
for i in all_lears:
	if i in dict1:
		dict1[i] += 1
	else:
		dict1[i] = 1

for i in dict1:
	if dict1[i] >= 5:
		print(f'YOU`ve GOT FLUSH! with {i}')
