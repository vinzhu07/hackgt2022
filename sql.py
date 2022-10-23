import pymysql.cursors

print("Connecting to RDS instance")

conn = pymysql.connect(host='buzzdash.cprggzpyeevc.us-east-1.rds.amazonaws.com',
                             user='root',
                             password='hackgt10-21-22',
                             db='buzzdash',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("Connected to RDS instance")

cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print("\nServer version:", row['VERSION()']) 
cursor.execute ("DROP TABLE if exists`Offer`;") 

conn.commit()


cursor.close()
conn.close()
