from bot import *
from SQL_ import *
from math import radians, cos, sin, asin, sqrt

cursor = Connect()

def setLang(lang_code):
    global lang
    lang = lang_code

def getLang():
    global lang
    return lang

"""def setCityID(city_ID):
    global CityID
    CityID = city_ID

def getCityID():
    global CityID
    return CityID"""

def setPointID(point_number):
    global PointID
    #print(getStartPointNum(getExcursionID()), int(str(getStartPointNum(getExcursionID())[0])[1:-2]))
    PointID = point_number

def getPointID():
    global PointID
    return int(PointID)

def setExcursionID(excursion_number):
    global ExcursionID
    ExcursionID = excursion_number

def getExcursionID():
    global ExcursionID
    return ExcursionID

def setMassOfMemorables(mass):
    global MassOfMemorables
    MassOfMemorables = mass

def getMassOfMemorables():
    global MassOfMemorables
    return MassOfMemorables

def language(message):
    """
    выбор языка
    :param message:
    :return:
    """
    markup_inline = types.InlineKeyboardMarkup()
    item_russian = types.InlineKeyboardButton(text = "Русский 🇷🇺", callback_data = 'ru')
    markup_inline.row(item_russian)
    item_english = types.InlineKeyboardButton(text = "English 🇬🇧", callback_data = 'en')
    markup_inline.row(item_english)
    bot.send_message(message.chat.id, "Choose a language\nВыберите язык", reply_markup= markup_inline)

def city(message):
    """
    выбор города
    :param message:
    :return: город
    """
    global CityID, lang
    markup_inline = types.InlineKeyboardMarkup()
    results = getCity(lang)
    CityID = 1
    for result in results:
        text = str(result)
        item = types.InlineKeyboardButton(text=text[2:len(text)-3], callback_data="City"+str(CityID))
        markup_inline.add(item)
        CityID += 1
    bot.delete_message(message.chat.id, message.message_id)
    if lang == 'en':
        bot.send_message(message.chat.id, "Chose city", reply_markup= markup_inline)
    if lang == 'ru':
        bot.send_message(message.chat.id, "Выберете город", reply_markup= markup_inline)

def ChangeCity(message):
    """
    смена города
    :param massege:
    :return:
    """
    global CityID, lang
    markup_inline = types.InlineKeyboardMarkup()
    results = getCity(lang)
    CityID = 1
    for result in results:
        text = str(result)
        item = types.InlineKeyboardButton(text=text[2:len(text)-3], callback_data="City"+str(CityID))
        markup_inline.add(item)
        CityID += 1
    if lang == 'en':
        bot.send_message(message.chat.id, "Chose city", reply_markup= markup_inline)
    if lang == 'ru':
        bot.send_message(message.chat.id, "Выберете город", reply_markup= markup_inline)


def route(message):
    """
    выводит список экскурсий
    :param message:
    :return:
    """
    markup_inline = types.InlineKeyboardMarkup()
    results = getRouteShortInfo(lang)
    routeID = 1
    text_choose_route = ''
    for result in results:
        text = str(result[0]) + "  " + str(result[1]) + "★"
        item = types.InlineKeyboardButton(text=text, callback_data="Route"+str(routeID))
        markup_inline.add(item)
        routeID += 1
    if lang == 'en':
        text_choose_route = 'Choose route'
    if lang == 'ru':
        text_choose_route = 'Выберите экскурсию'
    bot.send_message(message.chat.id, text_choose_route, reply_markup= markup_inline)

def PushRoute(message, ExcID):
    """
    выводит информацию про экскурсию + возможность начать/вернуться
    :param message:
    :param ExcID:
    :return:
    """
    markup_inline = types.InlineKeyboardMarkup()
    results = getRouteInfo(getLang(), ExcID)
    # start_point = getPointCoord(ExcID)
    text_back = ""
    text_start = ""
    text_send = ""
    text_time = ""
    text_LongWay = ""
    text_map_photo = ""
    text_map_link = ""
    # text_start_point = ""
    if getLang() == 'ru':
        text_back = "Назад"
        text_start = "Начать"
        text_time = "Время: "
        text_LongWay = "Расстояние: "
        text_map_link = 'Фото карты'
        text_map_photo = 'Яндекс карты'
        # text_start_point = "Стартовая точка экскурсии:"
    if getLang() == 'en':
        text_back = "Back"
        text_start = "Start"
        text_time = "Time: "
        text_LongWay = "Distance: "
        text_map_link = 'Map photo'
        text_map_photo = 'Yandex map'
        # text_start_point = "Start point:"
    for i in range(len(results[0])):
        text_send = "*" + results[0][0] + "*\n\n"  # Name
        text_send += "_" + results[0][1] + "_\n\n"  # Description
        text_send += "🕘" + text_time + str(results[0][2]) + "\n\n"  # Time
        text_send += "🗺" + text_LongWay + str(results[0][3])  # Distance
    MapInfo = getRouteMap(getExcursionID())
    item_back_excursions = types.InlineKeyboardButton(text=text_back, callback_data="back_excursions")
    item_start_excursion = types.InlineKeyboardButton(text=text_start, callback_data="start_excursion" + str(ExcID))
    markup_inline.add(item_back_excursions, item_start_excursion)
    item_map_link = types.InlineKeyboardButton(text=text_map_photo, url=MapInfo[0][1])  # Map_link
    markup_inline.row(item_map_link)
    text_send += f'\n\n[{text_map_link}⬇️]({MapInfo[0][0]})'  # Map_photo
    bot.send_message(message.chat.id, text_send, parse_mode="Markdown", reply_markup=markup_inline)
    # bot.send_message(message.chat.id, text_start_point)
    # bot.send_location(message.chat.id, start_point[0][0], start_point[0][1])

def PushContent(call, content_list):
    """
    Вывод содержания
    :param call:
    :param content_list:
    :return:
    """
    markup_inline = types.InlineKeyboardMarkup(row_width=5)
    PushText = ''
    PutButtonLine = []
    text_map_link = ''
    text_map_photo = ''
    MapInfo = getRouteMap(getExcursionID())
    if lang == 'ru':
        text_map_link = 'Фото карты'
        text_map_photo = 'Яндекс карты'
    if lang == 'en':
        text_map_link = 'Map photo'
        text_map_photo = 'Yandex map'
    for i in range(len(content_list)):
        PushText += "🔸" + str(content_list[i][0] -
                               int(str(getStartPointNum(getExcursionID())[0])[1:-2])) + " - "      #ID
        PushText += "" + content_list[i][1] + "\n"            #Name
        item_ID = types.InlineKeyboardButton(text = str(content_list[i][0] -
                                                        int(str(getStartPointNum(getExcursionID())[0])[1:-2])),
                                             callback_data = "contID" + str(content_list[i][0]))  #ID content
        PutButtonLine.append(item_ID)
    markup_inline.add(*PutButtonLine)
    item_map_link = types.InlineKeyboardButton(text = text_map_photo,
                                               url=MapInfo[0][1])   #Map_link
    markup_inline.row(item_map_link)
    PushText += f'\n[{text_map_link}⬇️]({MapInfo[0][0]})'       #Map_photo
    bot.send_message(call.message.chat.id, text=PushText, parse_mode="Markdown", reply_markup= markup_inline)

#def PushPoint(call, point, IsEnd):
    """
    Выводит инфомацию про точку(старая версия)
    Тип карты: геопозиция
    :param call:
    :param point: точка из SQL запроса
    :return:
    """
    """Point_ID = getPointID()
    PushText = "🔸" + str(point[Point_ID][0]) + "🔸\n"       #ID
    PushText += "📍*" + point[Point_ID][1] + "*\n\n"   #Name
    PushText += "_" + point[Point_ID][2] + "_"         #Description
    markup_inline_link = types.InlineKeyboardMarkup()
    text_sourse = ""
    text_NextPoint = ""
    text_question = ""
    text_content = ""
    text_rating = ""
    if lang == 'ru':
        text_sourse = "Источник"
        if IsEnd is False:
            text_NextPoint = "Далее"
        else:
            text_NextPoint = "Завершить экскурсию"
        text_question = "Идем дальше?"
        text_content = "Содержание"
        text_rating = "Оценить экскурсию"
    if lang == 'en':
        text_sourse = "Sourse"
        if IsEnd is False:
            text_NextPoint = "Next"
        else:
            text_NextPoint = "Finish"
        text_question = "Go on?"
        text_content = "Content"
        text_rating = "Rate the tour"
    item_sourse_link = types.InlineKeyboardButton(text = text_sourse, url=point[Point_ID][6])    #Link
    markup_inline_link.add(item_sourse_link)
    bot.send_message(call.message.chat.id, PushText, parse_mode="Markdown", reply_markup= markup_inline_link)
    photo_list = []
    photo = point[Point_ID][3]
    while photo != '':
        photo_list.append(InputMediaPhoto(media=photo.partition("\n")[0]))
        photo = photo.partition("\n")[2]
    bot.send_media_group(call.message.chat.id, media=photo_list)                        #Photo
    bot.send_location(call.message.chat.id, point[Point_ID][4], point[Point_ID][5])       #Point_width, Point_longitude
    markup_inline_next = types.InlineKeyboardMarkup()
    item_content = types.InlineKeyboardButton(text = text_content, callback_data = "content")  #Содержание
    item_next_point = types.InlineKeyboardButton(text = text_NextPoint,
                                                 callback_data = "PID" + str(point[Point_ID][0] + 1))  #PointID++
    if IsEnd is True:
        item_next_point.callback_data = 'menu'
    markup_inline_next.add(item_content, item_next_point)
    if IsEnd is True:
         item_rating = types.InlineKeyboardButton(text = text_rating,
                                                 callback_data = "set_rating")  #set_rating
         markup_inline_next.add(item_rating)
    bot.send_message(call.message.chat.id, text=text_question, reply_markup= markup_inline_next)"""

def PushPoint_New(call, point, IsEnd):
    """
    Выводит инфомацию про точку
    Тип карты: схема
    :param call:
    :param point: точка из SQL запроса
    :return:
    """
    Point_ID = getPointID() - int(str(getStartPointNum(getExcursionID())[0])[1:-2])
    text_map = ""
    text_sourse = ""
    text_NextPoint = ""
    text_question = ""
    text_content = ""
    text_rating = ""
    if lang == 'ru':
        text_sourse = "Источник"
        if IsEnd is False:
            text_NextPoint = "Далее"
        else:
            text_NextPoint = "Завершить экскурсию"
        text_question = "Идем дальше?"
        text_content = "Содержание"
        text_rating = "Оценить экскурсию"
        text_map = "Путь до объекта"
    if lang == 'en':
        text_sourse = "Sourse"
        if IsEnd is False:
            text_NextPoint = "Next"
        else:
            text_NextPoint = "Finish"
        text_question = "Go on?"
        text_content = "Content"
        text_rating = "Rate the tour"
        text_map = "Схема движения"             #!!!!!!
    bot.send_photo(call.message.chat.id, point[Point_ID][5], caption=text_map)  # map_scheme
    PushText = "🔸" + str(point[Point_ID][0] -
                          int(str(getStartPointNum(getExcursionID())[0])[1:-2])) + "🔸\n"       #ID
    PushText += "📍<b>" + point[Point_ID][1] + "</b>\n\n"   #Name
    PushText += "<i>" + point[Point_ID][2] + "</i>"         #Description
    markup_inline_link = types.InlineKeyboardMarkup()
    item_sourse_link = types.InlineKeyboardButton(text = text_sourse, url=point[Point_ID][4])    #Link
    markup_inline_link.add(item_sourse_link)
    bot.send_message(call.message.chat.id, PushText, parse_mode="HTML", reply_markup= markup_inline_link)
    photo_list = []
    photo = point[Point_ID][3]                                                  #Photo
    while photo != '':
        photo_list.append(InputMediaPhoto(media=photo.partition("\n")[0]))
        photo = photo.partition("\n")[2]
    bot.send_media_group(call.message.chat.id, media=photo_list)
    markup_inline_next = types.InlineKeyboardMarkup()
    item_content = types.InlineKeyboardButton(text = text_content, callback_data = "content")  #Содержание
    item_next_point = types.InlineKeyboardButton(text = text_NextPoint,
                                                 callback_data = "PID" + str(point[Point_ID][0] + 1))  #PointID++
    if IsEnd is True:
        item_next_point.callback_data = 'menu'
    markup_inline_next.add(item_content, item_next_point)
    if IsEnd is True:
         item_rating = types.InlineKeyboardButton(text = text_rating,
                                                 callback_data = "set_rating")  #set_rating
         markup_inline_next.add(item_rating)
    bot.send_message(call.message.chat.id, text=text_question, reply_markup= markup_inline_next)


def menu(message):
    """
    выводит клавиатуру с меню
    :param message:
    :return:
    """
    text_menu = ''
    text_change = ''
    text_route = ''
    text_near = ''
    if lang == 'en':
        text_menu = 'Menu'
        text_change = 'Change city'
        text_route = 'Excursions'
        text_near = 'Nearest excursion'
    if lang == 'ru':
        text_menu = 'Меню'
        text_change = 'Сменить город'
        text_route = 'Экскурсии'
        text_near = 'Ближайшая экскурсия'
    bot.delete_message(message.chat.id, message.message_id)
    markup_replay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_newCity = types.KeyboardButton(text = text_change)
    item_excursions = types.KeyboardButton(text = text_route)
    item_nearExc = types.KeyboardButton(text=text_near, request_location=True)
    markup_replay.add(item_excursions, item_newCity)
    markup_replay.add(item_nearExc)
    bot.send_message(message.chat.id, text_menu, reply_markup= markup_replay)


def distance_points(lat1, lon1, lat2, lon2):
    """
    источник: https://qna.habr.com/q/402062?ysclid=l78q10jtqt448757757

    Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
    https://en.wikipedia.org/wiki/Haversine_formula
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km