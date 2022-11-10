from callback_func import *


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    главный метод для обработки текста в чате
    :param message:
    :return:
    """
    if message.text.lower() == "привет" or message.text.lower() == 'hi':
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower() == "menu" or message.text.lower() == "меню":
        menu(message)
    elif message.text.lower() == '/start':
        language(message)
        PutUserID(message.from_user.id)
    elif message.text.lower() == "excursions" or message.text.lower() == "экскурсии":
        route(message)
    elif message.text.lower() == "change city" or message.text.lower() == "сменить город":
        ChangeCity(message)
    elif message.from_user.id == 499671735:
        if message.text.lower() == "!реклама":
            """создать таблицу ad_data(title, text, ref)
            создать метод по предварительному показ сообщения
            создать метод для рассылки рекламного сообщения"""
        elif message.text.lower() == 'тульская':
            bot.send_location(message.chat.id, 55.708841, 37.622621)
            bot.send_message(message.chat.id, "⬇️🔽⏬*bold* _italic_ \n `fixed width font` [link](http://yandex.ru)",
                             parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           "https://pastvu.com/_p/a/4/e/e/4eeb776b5100f285bdf534cc15edcc1d.jpg")
            bot.send_message(message.chat.id, f"{message.from_user.id} {message.from_user.username}")
            bot.send_message(message.chat.id, text="<b>Сам жирный</b>\n<i>Курсив</i>\n<code>код</code>\n"
                                                   "<s>перечеркнутый</s>\n<u>подчеркнутый</u>\n"
                                                   "<pre language=\"c++\">код</pre>\n<a href=\"smth.ru\">Сайт</a>",
                             parse_mode="HTML")


bot.polling(none_stop=True, interval=0)