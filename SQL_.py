import psycopg2
from datetime import datetime


"""def Connect():
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    return cursor"""


def Connect():
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    return cursor

def getCity(lang):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = """SELECT Name_ru FROM City"""
    if lang == 'en':
        sql = """SELECT Name FROM City"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getRouteShortInfo(lang):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = """SELECT Name_ru, Rating_mark FROM Route ORDER BY id"""
    if lang == 'en':
        sql = """SELECT Name, Rating_mark FROM Route ORDER BY id"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getRouteInfo(lang, ID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = f"""SELECT Name_ru, Description_ru, Time, LongWay FROM Route WHERE ID = {ID}"""
    if lang == 'en':
        sql = f"""SELECT Name, Description, Time, LongWay FROM Route WHERE ID = {ID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getRouteMap(ID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    sql = f"""SELECT Map_photo, Map_link FROM Route WHERE ID = {ID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def getMemorable(lang):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = """SELECT Name_ru FROM Memorable_new"""
    if lang == 'en':
        sql = """SELECT Name FROM Memorable_new"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def excursion_points(lang, ExcID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = f"""SELECT ID, Name_ru, Description_ru, Photo, Point_width, Point_longitude, Link
        FROM memorable
        JOIN communication ON public.communication.memorableid = public.memorable.id 
        WHERE communication.RouteID = {ExcID}"""
    if lang == 'en':
        sql = f"""SELECT ID, Name, Description, Photo, Point_width, Point_longitude, Link 
        FROM memorable 
        JOIN communication ON communication.memorableid = memorable.id 
        WHERE communication.RouteID = {ExcID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def excursion_points_new(lang, ExcID):
    """

    :param lang:
    :param ExcID:
    :return: 0 - ID, 1 - Name_ru, 2 - Description_ru, 3 - Photo, 4 - Link, 5 - map_scheme
    """
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = f"""SELECT ID, Name_ru, Description_ru, Photo, Link, Map_scheme
        FROM memorable_new
        JOIN communication ON communication.memorableid = memorable_new.id
        WHERE communication.RouteID = {ExcID}"""
    if lang == 'en':
        sql = f"""SELECT ID, Name, Description, Photo, Link, map_scheme
        FROM memorable_new 
        JOIN communication ON communication.memorableid = memorable_new.id
        WHERE communication.RouteID = {ExcID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def excursion_content(lang, ExcID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = ''
    if lang == 'ru':
        sql = f"""SELECT ID, Name_ru
        FROM memorable_new
        INNER JOIN communication ON communication.MemorableID = Memorable_new.ID
        WHERE communication.RouteID = {ExcID}"""
    if lang == 'en':
        sql = f"""SELECT ID, Name
        FROM memorable_new 
        INNER JOIN communication ON communication.MemorableID = Memorable_new.ID 
        WHERE communication.RouteID = {ExcID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def setRating(ExcID, raiting, user_info, date_message):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""DELETE FROM rating WHERE route_id = {ExcID} AND user_id = {user_info.id}"""
    cursor.execute(sql)
    # конвератция времени выставления оценки из unix time в обычное
    date_time = str(datetime.utcfromtimestamp(date_message).strftime('%Y-%m-%d %H:%M:%S'))
    date = date_time[:10:]
    cursor.execute(
        """INSERT INTO rating(route_id, rating_data, user_id, user_name, message_date) 
        VALUES('%s', '%s', '%s', '%s', '%s')""" % (ExcID, raiting, user_info.id, str(user_info.username), date))
    con.commit()
    calculateRating(ExcID)

def calculateRating(ExcID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password ='12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""SELECT rating_data FROM rating WHERE route_id = {ExcID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    summ = 0
    for i in range(len(result)):
        res = str(result[i])
        res = res[1:2]
        summ += int(res)
    sred_aref = round(summ / len(result), 2)
    sql = f"""UPDATE route SET Rating_mark = {sred_aref} WHERE id = {ExcID}"""
    cursor.execute(sql)
    con.commit()

def getRating():
    con = psycopg2.connect(
        host='localhost',
        user='vladimirfilimonov',
        password='12345678',
        database='excursion_bot'
    )
    cursor = con.cursor()
    sql = """SELECT Rating_mark FROM route ORDER BY id"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getStartPointNum(ExcID):
    con = psycopg2.connect(
        host='localhost',
        user='vladimirfilimonov',
        password='12345678',
        database='excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""SELECT start_point_num FROM route WHERE id = {ExcID}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getPointCoord(PointNum):
    con = psycopg2.connect(
        host='localhost',
        user='vladimirfilimonov',
        password='12345678',
        database='excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""SELECT point_width, point_longitude FROM memorable_new WHERE id = {PointNum}"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getStartPointCoord():
    con = psycopg2.connect(
        host='localhost',
        user='vladimirfilimonov',
        password='12345678',
        database='excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""SELECT start_point_coord_lon, start_point_coord_lat, id FROM route"""     #ORDER BY id
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def PutUserID(UID):
    con = psycopg2.connect(
        host = 'localhost',
        user = 'vladimirfilimonov',
        password = '12345678',
        database = 'excursion_bot'
    )
    cursor = con.cursor()
    sql = f"""DELETE FROM users_id WHERE id = {UID}"""
    cursor.execute(sql)
    cursor.execute("""INSERT INTO users_id(id) VALUES('%s')""" % (UID))
    con.commit()