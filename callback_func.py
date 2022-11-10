from functions import *

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data[:3]=='PID':
        PlusPointID(call)
    elif call.data[:4]=='City':
        call_menu(call)
    elif call.data[:5]=='Route':
        setExcursionID(call.data[5::])
        call_route(call)
    elif call.data[:15]=='start_excursion':
        start_excursion(call)
    elif call.data=='back_excursions':
        back_excursions(call)
    elif call.data == 'menu':
        menu(call.message)
    elif call.data[:7]=='content':
        content(call)
    elif call.data[:6] =='contID':
        PlusPointID_content(call)
    elif call.data == 'set_rating':
        call_setRating(call)
    elif call.data[:4] == 'rait':
        setRating(getExcursionID(), call.data[4::], call.from_user, call.message.date)
        menu(call.message)
    elif call.data=='ru':
        lang_rus(call)
    elif call.data=='en':
        lang_en(call)

@bot.message_handler(content_types=["location"])
def call_FindNearestExc(message):
    """
    поиск ближайшей экскурсии
    :param message:
    :return:
    """
    if message.location is not None:
        ExcPoints = getStartPointCoord()
        ExcDistance = {a: 0 for a in range(len(ExcPoints[0]))}
        for i in range(len(ExcPoints[0])):
            ExcDistance[i] = int(distance_points(message.location.latitude, message.location.longitude,
                                               ExcPoints[i][0], ExcPoints[i][1]))
        ExcDistance = sorted(ExcDistance.items(), key=lambda x: x[1])
        setExcursionID(ExcDistance[0][0])
        PushRoute(message, ExcDistance[0][0])



def lang_rus(call):
    """

    :param call:
    :return: устанавливает русский язык
    """
    setLang('ru')
    city(call.message)

def lang_en(call):
    """

    :param call:
    :return: устанавливает английский язык
    """
    setLang('en')
    city(call.message)

def call_menu(call):
    """
    когда выбрали город вызывает меню
    :param call:
    :return:
    """
    menu(call.message)

def call_setRating(call):
    """
    Высылает ссобщение с просьбой выставить рейтинг
    :param call:
    :return:
    """
    text_answer = ''
    if getLang() == 'ru':
        text_answer = 'Поставьте оценку по 5-и бальной шкале'
    if getLang() == 'en':
        text_answer = 'Put a rating on the 5th scale'
    markup_inline = types.InlineKeyboardMarkup()
    for i in range(5):
        i += 1
        item_rat_num = types.InlineKeyboardButton(text = str(i) + '★', callback_data = "rait" + str(i))
        markup_inline.row(item_rat_num)
    bot.send_message(call.message.chat.id, text_answer, reply_markup=markup_inline)

def call_route(call):
    """
    вызывает метод вывода информаци про экскурсию + возможность начать/вернуться
    :param call:
    :return:
    """
    PushRoute(call.message, call.data[5::])


def back_excursions(call):
    """
    вернуться к списку экскурсий
    :param call:
    :return:
    """
    route(call.message)


def start_excursion(call):
    """
    начать экскурсию
    :param call:
    :return:
    """
    setPointID(int(str(getStartPointNum(getExcursionID()))[2:-3]))
    setExcursionID(call.data[15:])
    #setMassOfMemorables(excursion_points(getLang(), getExcursionID()))
    setMassOfMemorables(excursion_points_new(getLang(), getExcursionID()))
    PushPoint_New(call, getMassOfMemorables(), False)

def PlusPointID(call):
    """
    меняет значение PointID
    :param call:
    :return:
    """
    setPointID(int(call.data[3::]) - 1)
    IsEnd = False
    if len(getMassOfMemorables()) - 1 == getPointID() - int(str(getStartPointNum(getExcursionID())[0])[1:-2]):
        IsEnd = True
    PushPoint_New(call, getMassOfMemorables(), IsEnd)

def PlusPointID_content(call):
    """
    меняет значение PointID, но с другим обрезанием
    :param call:
    :return:
    """
    setPointID(int(call.data[6::]) - 1)
    IsEnd = False
    if len(getMassOfMemorables()) - 1 == getPointID() - int(str(getStartPointNum(getExcursionID())[0])[1:-2]):
        IsEnd = True
    PushPoint_New(call, getMassOfMemorables(), IsEnd)

def content(call):
    """
    вызов метода вывода экскурсий
    :param call:
    :return:
    """
    content_list = excursion_content(getLang(), getExcursionID())
    PushContent(call, content_list)

