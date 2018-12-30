import pymysql
import random


connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='newpassword', db='transportation',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)

mycursor = connection.cursor()


type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']

sql = "insert into Proposer(num, Mileage, Date, CType_id, isRecived) values(%d, %d, now(), %s , 0);"\
      %(random.randint(20, 500),random.randint(100, 10000) ,random.choice(type_list))

# sql = "show full columns in transportation.Proposer;"

mycursor.execute(sql)
result = mycursor.fetchall()

connection.commit()

