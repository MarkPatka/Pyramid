create database hotel;
use hotel;

create table rooms (
id_room int (5) AUTO_INCREMENT,
room_number int(5) NOT NULL,
room_type text NOT NULL,
cost_per_night int(5) NOT NULL,
PRIMARY KEY (id_room) 
);

create table guests (
id_guest int (10) AUTO_INCREMENT,
guest_name text NOT NULL,
guest_email varchar(50),
guest_DoB date NOT NULL, 
guest_in date NOT NULL,
guest_out date NOT NULL,
FOREIGN KEY (id_guest) REFERENCES rooms (id_room)
);

create table admins (
id_admin int (10) AUTO_INCREMENT,
admin_name text (30) NOT NULL,
FOREIGN KEY (id_admin) REFERENCES guests (id_guest)
);

create table cleaners (
cleaner_id int (5) AUTO_INCREMENT,
cleaner_name text NOT NULL,
FOREIGN KEY (cleaner_id) REFERENCES rooms (id_room)
);

INSERT INTO rooms VALUES ('1', '001', 'single', '1800');
INSERT INTO rooms (room_number, room_type, cost_per_night) VALUES 
('002','double','2300'),
('003','luxe','4200');

INSERT INTO guests (guest_name, guest_email, guest_DoB, guest_in, guest_out) VALUES 
('Поставьте Марку Патка', 'mark.kaz.1998@gmail.com', '1998.12.27', '2020.01.12', '2020.01.30'),
('Пожалуйста Хотя Бы', 'sem.sech@pupa.com', '1998.12.27', '2020.01.12', '2020.01.30'),
('Тройку Очень Прошувич', 'cha.cha@chto.ru', '1998.12.27', '2020.01.12', '2020.01.30');

INSERT INTO admins (admin_name) VALUES
('Zagonyailo Cto-to Neadekvat'),
('Vtirailo Kakyeto Dich'),
('Hlebaito S Gorya');

INSERT INTO cleaners (cleaner_name) VALUES
('Horosho Polo Moito'),
('Neploho Belie Postiraito'),
('Vkysno Kyshat Gotovilo');

#Упорядочил список номеров по их стоимости в порядке убывания
SELECT * FROM rooms ORDER BY cost_per_night DESC;
#Выбрал номер класса "люкс" обращением к его id
SELECT room_type FROM rooms WHERE id_room>2;
#вывел в новую таблици информацию о номере (тип номера, номер, кто в нем проживает)
SELECT rooms.room_type, rooms.room_number, guests.guest_name
FROM rooms, guests
WHERE rooms.id_room = guests.id_guest;
#Прикрепил определенные номера за определенными уборщиками
SELECT cleaners.cleaner_name, rooms.room_number
FROM cleaners LEFT OUTER JOIN rooms
ON cleaners.cleaner_id = rooms.id_room;
#Посчитал сколько всего классов номеров в отеле
SELECT COUNT(room_type) FROM rooms;
#Посчитал сколько номеров каждого из классов(сюкс, сингл, дабл) в отеле
SELECT room_type, COUNT(room_type) FROM rooms
GROUP BY room_type;
#Добавил столбец содержащий информацию о трудовом стаже одного из администраторов
ALTER TABLE admins ADD COLUMN seniority varchar(20) AFTER admin_name;

UPDATE admins SET seniority = '30'
WHERE id_admin = 2;
#Посчитал доход отеля в день при полной загруженности отеля.
SELECT SUM(cost_per_night) FROM rooms;
#Считал из файла инфо об отеле
SELECT LOAD_FILE("C:/DataBaseTask/hotel.txt");
#Продлил время пребывания для одного из гостей на 3 дня
SELECT id_guest, guest_in FROM guests;
SELECT id_guest, ADDDATE(guest_in, INTERVAL +3 DAY)
FROM guests
WHERE id_guest=2;
#Вывел сегодняшнюю дату в привычном виде
SELECT DATE_FORMAT(CURDATE(), '%d.%m.%Y');
