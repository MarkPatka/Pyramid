#Task01

quant_cups = int(input('Сколько чашек кофе вы желаете приобрести? '))
bonus_cups = quant_cups // 6
print("Вы можете получить ", bonus_cups, "бесплатных чашек кофе")

#Task 02
coord1 = input('Укажите координаты первой точки через \";\": ')
coord1 = coord1.split(';')
x1 = int(coord1[0])
y1 = int(coord1[1])
coord2 = input('Укажите координаты второй точки через \";\" ')
coord2 = coord2.split(';')
x2 = int(coord2[0])
y2 = int(coord2[1])
print("M1 = ", coord1, "M2 = ", coord2)
A = x2 - x1
B = y2 - y1
length = ((A**2)+(B**2))**0.5
print("Расстояние между точками равно: {length:1.2f}".format(length=length))

#Task03
cows = int(input("Скока у тебя коров? "))
chickens = int(input("Скока у тя кур? "))
pigs = int(input("Скока у тя хряков? "))
cowlegs = cows * 4
chicklegs = chickens * 2
piglegs = pigs * 4
legs = cowlegs + piglegs + chicklegs
print(legs)