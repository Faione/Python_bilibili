import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456789',
                             db='bdata',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def insert_to_b3_qgfx(data, bv, title, jj, review):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `b3_qgfx` (`DATE`, `BV`, `TITLE`, `JJ`, `REVIEW`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data, bv, title, jj, review))
        connection.commit()


def insert_to_hd_cyfx(tag, id_up, bv, count_coin, count_zan, count_sc, count_bf):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `hd_cyfx` (`TAG`, `ID_UP`, `BV`, `COUNT_COIN`, `COUNT_ZAN`, `COUNT_SC`, `COUNT_BF`" \
              ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (tag, id_up, bv, count_coin, count_zan, count_sc, count_bf))
        connection.commit()

