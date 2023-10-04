import psycopg2

conn = psycopg2.connect(dbname="student", host="192.168.1.47", user="student", password="root", port="5432")

cursor = conn.cursor()
# cursor.execute("""
#     CREATE TABLE moderators (
#         id INT PRIMARY KEY,
#         name VARCHAR(30)
#     )
# """)
# cursor.execute("""
#     CREATE TABLE users (
#         id INT PRIMARY KEY,
#         name VARCHAR(30)
#     )
# """)
# cursor.execute("""
    # CREATE TABLE request (
    #     id INT PRIMARY KEY,
    #     status VARCHAR(10),
    #     date_create DATE,
    #     date_formation DATE,
    #     date_complete DATE,
    #     id_user INT,
    #     id_moderator INT,
    #     FOREIGN KEY (id_user) REFERENCES users(id),
    #     FOREIGN KEY (id_moderator) REFERENCES moderators(id)
    # );
# """)
# cursor.execute("""    CREATE TABLE orders (
#     id INTEGER PRIMARY KEY,
#     title TEXT,
#     src TEXT,
#                definition_id INT,
#     FOREIGN KEY (definition_id) REFERENCES info_orders(id),
#     status TEXT
# );""")


cursor.execute("""INSERT INTO mm_orders_requests (orders_id, requests_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 6),
    (4, 1),
    (4, 3),
    (5, 2),
    (5, 4),
    (6, 5),
    (6, 6);""")

conn.commit()   # реальное выполнение команд sql1
 
cursor.close()
conn.close()