import telebot
from config import TOKEN, valute
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


#обработчик команд start и help
@bot.message_handler(commands=['start', 'help'])
def begin(message):
    bot.send_message(message.chat.id, 'Приветствую, в данном боте вы имеете следующие возможности: \n'
                                      'Вводить команды:\n'
                                      '/start - Начало работы с ботом\n'
                                      '/help - Запрос начальной инструкции\n'
                                      '/valute - Отобразить валюты возможные к кновертации\n'
                                      '/currency - Инструкция для конвертации\n')


#вывод валют с которыми можно работать
@bot.message_handler(commands=['valute'])
def valute_contain(message):
    text = 'Доступные валюты:'
    for key in valute.keys():
        text = '\n'.join((text, f'{key} - {valute[key]}'))
    bot.send_message(message.chat.id, text)


#Пример и помощь в конвертации валют
@bot.message_handler(commands=['currency'])
def get_currency(message):
    bot.send_message(message.chat.id, f'Введите данные в формате:\n'
                                      f'<Валюта которую собираетесь конвертировать> '
                                      f'<Валюта в которую собираетсь конвертировать> '
                                      f'<количество валюты>\n\n'
                                      f'Например: доллар рубль 100\n\n'
                                      f'При вводе дробных чисел используйте точку\n\n'
                                      f'Названия валют должны начинаться с маленькой буквы')


#Обработки конвертации
@bot.message_handler()
def convert(message):
    query = message.text.split(' ')
    try:
        if len(query) != 3:
            raise APIException('Вы неверно ввели запрос, должно быть 3 слова')
        base, quote, amount = query
        amount_query = str(format(Converter.get_price(base, quote, amount), '.2f'))
        #преобразую выходные данные в строку с двумязнаками после запятой

        reply = f'{base} в количесвте {amount} равен {amount_query} {quote}'
    except APIException as e:
        bot.reply_to(message, f'Ошибка введенных данных\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера, не получается обработать команду\n{e}')

    else:
        bot.reply_to(message, reply)


bot.polling()
