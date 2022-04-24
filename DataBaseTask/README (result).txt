mysql> create database hotel;
Query OK, 1 row affected (0.03 sec)

mysql> use hotel;
Database changed
mysql>
mysql> create table rooms (
    -> id_room int (5) AUTO_INCREMENT,
    -> room_number int(5) NOT NULL,
    -> room_type text NOT NULL,
    -> cost_per_night int(5) NOT NULL,
    -> PRIMARY KEY (id_room)
    -> );
Query OK, 0 rows affected (0.10 sec)

mysql>
mysql> create table guests (
    -> id_guest int (10) AUTO_INCREMENT,
    -> guest_name text NOT NULL,
    -> guest_email varchar(50),
    -> guest_DoB date NOT NULL,
    -> guest_in date NOT NULL,
    -> guest_out date NOT NULL,
    -> FOREIGN KEY (id_guest) REFERENCES rooms (id_room)
    -> );
Query OK, 0 rows affected (0.10 sec)

mysql>
mysql> create table admins (
    -> id_admin int (10) AUTO_INCREMENT,
    -> admin_name text (30) NOT NULL,
    -> FOREIGN KEY (id_admin) REFERENCES guests (id_guest)
    -> );
Query OK, 0 rows affected (0.07 sec)

mysql>
mysql> create table cleaners (
    -> cleaner_id int (5) AUTO_INCREMENT,
    -> cleaner_name text NOT NULL,
    -> FOREIGN KEY (cleaner_id) REFERENCES rooms (id_room)
    -> );
Query OK, 0 rows affected (0.07 sec)

mysql>
mysql> INSERT INTO rooms VALUES ('1', '001', 'single', '1800');
Query OK, 1 row affected (0.05 sec)

mysql> INSERT INTO rooms (room_number, room_type, cost_per_night) VALUES
    -> ('002','double','2300'),
    -> ('003','luxe','4200');
Query OK, 2 rows affected (0.06 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql>
mysql> INSERT INTO guests (guest_name, guest_email, guest_DoB, guest_in, guest_out) VALUES
    -> ('Марк Патка', 'mark.kaz.1998@gmail.com', '1998.12.27', '2020.01.12', '2020.01.30'),
    -> ('Хотя Бы', 'sem.sech@pupa.com', '1998.12.27', '2020.01.12', '2020.01.30'),
    -> ('4 Очень Прошувич', 'cha.cha@chto.ru', '1998.12.27', '2020.01.12', '2020.01.30');
Query OK, 3 rows affected (0.04 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql>
mysql> INSERT INTO admins (admin_name) VALUES
    -> ('Zagonyailo Cto-to Neadekvat'),
    -> ('Vtirailo Kakyeto Dich'),
    -> ('Hlebaito S Gorya');
Query OK, 3 rows affected (0.05 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql>
mysql> INSERT INTO cleaners (cleaner_name) VALUES
    -> ('Horosho Polo Moito'),
    -> ('Neploho Belie Postiraito'),
    -> ('Vkysno Kyshat Gotovilo');
Query OK, 3 rows affected (0.04 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql>
mysql> SELECT * FROM rooms ORDER BY cost_per_night DESC;
+---------+-------------+-----------+----------------+
| id_room | room_number | room_type | cost_per_night |
+---------+-------------+-----------+----------------+
|       3 |           3 | luxe      |           4200 |
|       2 |           2 | double    |           2300 |
|       1 |           1 | single    |           1800 |
+---------+-------------+-----------+----------------+
3 rows in set (0.00 sec)

mysql>
mysql> SELECT room_type FROM rooms WHERE id_room>2;
+-----------+
| room_type |
+-----------+
| luxe      |
+-----------+
1 row in set (0.00 sec)

mysql>
mysql> SELECT rooms.room_type, rooms.room_number, guests.guest_name
    -> FROM rooms, guests
    -> WHERE rooms.id_room = guests.id_guest;
+-----------+-------------+-----------------------+
| room_type | room_number | guest_name            |
+-----------+-------------+-----------------------+
| single    |           1 | Поставьте Марку Патка |
| double    |           2 | Пожалуйста Хотя Бы    |
| luxe      |           3 | Тройку Очень Прошувич |
+-----------+-------------+-----------------------+
3 rows in set (0.00 sec)

mysql>
mysql> SELECT cleaners.cleaner_name, rooms.room_number
    -> FROM cleaners LEFT OUTER JOIN rooms
    -> ON cleaners.cleaner_id = rooms.id_room;
+--------------------------+-------------+
| cleaner_name             | room_number |
+--------------------------+-------------+
| Horosho Polo Moito       |           1 |
| Neploho Belie Postiraito |           2 |
| Vkysno Kyshat Gotovilo   |           3 |
+--------------------------+-------------+
3 rows in set (0.00 sec)

mysql>
mysql> SELECT COUNT(room_type) FROM rooms;
+------------------+
| COUNT(room_type) |
+------------------+
|                3 |
+------------------+
1 row in set (0.00 sec)

mysql>
mysql> SELECT room_type, COUNT(room_type) FROM rooms
    -> GROUP BY room_type;
+-----------+------------------+
| room_type | COUNT(room_type) |
+-----------+------------------+
| double    |                1 |
| luxe      |                1 |
| single    |                1 |
+-----------+------------------+
3 rows in set (0.05 sec)

mysql>
mysql> ALTER TABLE admins ADD COLUMN seniority varchar(20) AFTER admin_name;
Query OK, 3 rows affected (0.25 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql>
mysql> UPDATE admins SET seniority = '30'
    -> WHERE id_admin = 2;
Query OK, 1 row affected (0.04 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql>
mysql> SELECT SUM(cost_per_night) FROM rooms;
+---------------------+
| SUM(cost_per_night) |
+---------------------+
|                8300 |
+---------------------+
1 row in set (0.00 sec)

mysql>
mysql> SELECT LOAD_FILE("C:/DataBaseTask/hotel.txt");
+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| LOAD_FILE("C:/DataBaseTask/hotel.txt")                                                                                                                             |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Hotel Information
==================
The hotel was buid in my (Patka M.A) mind and It has 3 rooms as I have 3 meanders.
==================
That is all. |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql>
mysql> SELECT id_guest, guest_in FROM guests;
+----------+------------+
| id_guest | guest_in   |
+----------+------------+
|        1 | 2020-01-12 |
|        2 | 2020-01-12 |
|        3 | 2020-01-12 |
+----------+------------+
3 rows in set (0.00 sec)

mysql> SELECT id_guest, ADDDATE(guest_in, INTERVAL +3 DAY)
    -> FROM guests
    -> WHERE id_guest=2;
+----------+------------------------------------+
| id_guest | ADDDATE(guest_in, INTERVAL +3 DAY) |
+----------+------------------------------------+
|        2 | 2020-01-15                         |
+----------+------------------------------------+
1 row in set (0.00 sec)

mysql>
mysql> SELECT DATE_FORMAT(CURDATE(), '%d.%m.%Y');
+------------------------------------+
| DATE_FORMAT(CURDATE(), '%d.%m.%Y') |
+------------------------------------+
| 23.01.2020                         |
+------------------------------------+
1 row in set (0.00 sec)
