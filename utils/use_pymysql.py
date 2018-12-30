import pymysql
import random
from random import choice, randint
from datetime import timedelta
from django.utils import timezone


connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='newpassword', db='transportation',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)

mycursor = connection.cursor()


def get_cno():
    s = choice(choice_list)+randint(1001, 9999).__str__()
    return s


choice_list = ['豫B', '冀D', '豫E', '辽K', '皖A', '新B', '鲁N']
type_list = ['大型车', '中型车', '小型车', '公交车', '长途车']
coil_comsuption = {'大型车':1000, '中型车': 600, '小型车': 300, '公交车':200, '长途车': 350}
phone_first = ['155', '156', '181', '188', '136', '159', '137', '189', '177']
spot_list = ['市中心', '立交桥', '高速公路', '不详', '乡村小道']
cause_list = ['司机酒驾', '追尾', '超速驾驶', '超车事故', '天气因素', '疲劳驾驶', '不详']
money_list = [100, 200, 2000, 5000, 10000, 20000, 30000, 60000]


sql = "insert into Record ( STime, ETime, OilConsumpution, isDelete, CNo_id, DName_id, DNo_id)" \
      "values (now(), %s, %d, false, %s, %d );" %(timezone.now() + timedelta(days=random.randint(10, 200)),
                                           choice([1000, 600, 300, 200, 350]),
                                           get_cno(), randint(1000)
                                        )


# sql = "show full columns in transportation.Proposer;"
for i in range(100):
    mycursor.execute(sql)
    # result = mycursor.fetchall()

connection.commit()
