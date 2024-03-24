import pyodbc
from datetime import datetime

print("helloy")

ADMIN_CHAT_ID = ["",""]

#connekt database

try:
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\geime\Desktop\vpn2.0\base.accdb;'
    conn = pyodbc.connect(con_string)
    print("Connected To Database")

except pyodbc.Error as e:
    print("Error in Connection database", e)


request_tariff = 'SELECT'+' * FROM base0'

cur = conn.cursor()
cur.execute(request_tariff)
 
for row in cur.fetchall():
        print(row)


#request_test_date = 'SELECT * FROM base0 WHERE id_chat_user = '+"'321321'"

#print ("gowna s polna")
#cur.execute(request_test_date)
#testdatetime = cur.fetchall()
#print(testdatetime[0][5].strftime("%d/%m/%y"))


def request_term(id_chat_user):
    request_date = 'SELECT * FROM base0 WHERE id_chat_user = ' + id_chat_user
    cur.execute(request_date)
    date_time = cur.fetchall()
    print(date_time[0][5].strftime("%d/%m/%y"))

#print(request_term("'123123'"))

def serch_user_sekure_key(secure_key):
     request_user_cekure = 'SELECT * FROM base0 WHERE pass_id = ' + secure_key
     cur.execute(request_user_cekure)
     user = cur.fetchall()
     if user:
        return user
     else:
        return "неверны код или юзера несуществует"

#serch_user_sekure_key(inputsekurecod)

def write_user_chat_id(user,chat_id):
    cur.execute('UPDATE base0 SET id_chat_user = ? WHERE user_key = ?', (chat_id, user))
    conn.commit()

testinsert = input("vvedi id chata")
write_user_chat_id("0001", testinsert)