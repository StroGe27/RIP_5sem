import psycopg2

conn = psycopg2.connect(dbname="student", host="192.168.0.204", user="student", password="root", port="5432")

cursor = conn.cursor()
# for _ in range(7):
#     cursor.execute(f"""UPDATE orders SET processor = '{orders_arr['title']}', ghz = '{}', ram = '{}' WHERE id = '{}';""", 1, 2, 3, 4)

# print(cursor.fetchall())



# UPDATE orders SET ghz = 'value', ram = 'value' WHERE id = 'value';
orders_arr = [
    {'title': 'EL11-SSD-10GE', 'id': 1, 'src': '/images/1.jpg', 'processor': 'Intel Xeon E-2236', "Ghz": 3.5, "cores": 6, "ram": 32},
    {'title': 'EL42-NVMe', 'id': 2, 'src': 'images/2.jpg', 'processor': 'Intel Xeon E-2386G', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'title': 'EL13-SSD', 'id': 3, 'src': 'images/3.jpg', 'processor': 'Intel Xeon E-2236', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'title': 'BL22-NVMe', 'id': 4, 'src': 'images/4.jpg', 'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 128},
    {'title': 'BL21R-NVMe', 'id': 5, 'src': 'images/5.jpg', 'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 256},
    {'title': 'PL25-NVMe', 'id': 6, 'src': 'images/6.jpg', 'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 256},
    {'title': 'PL25-NVMe_1', 'id': 7, 'src': 'images/6.jpg', 'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 254},
]
orders_arrs = [
    {'cost': '11900'},
    {'cost': '15600'},
    {'cost': '16800'},
    {'cost': '34500'},
    {'cost': '49800'},
    {'cost': '7900'},
    {'cost': '4900'},
]

# for i in range(7):
#    cursor.execute("""UPDATE orders SET processor = '{}', ghz = '{}', ram = '{}' WHERE id = '{}';""".format(orders_arr[i]["processor"], orders_arr[i]["Ghz"], orders_arr[i]["ram"], i+1) )
for i in range(7):
   cursor.execute("""UPDATE orders SET cost = '{}' where id ={}""".format(orders_arrs[i]["cost"], i+1) )

# print(orders_arr[1]['title'])
conn.commit()   # реальное выполнение команд sql1
 
cursor.close()
conn.close()