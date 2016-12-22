import config
import telebot
from audio_loader import AudioLoader

bot = telebot.TeleBot(config.token)


class User():

    def __init__(self, id, first_name, last_name):
        self.id =id
        self.first_name = first_name
        self.last_name = last_name
        self.vk_id = 0

current_user = None

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    global current_user
    current_user = User(message.chat.id, message.chat.first_name, message.chat.last_name)
    bot.send_message(message.chat.id, 'Hello, {0}!'.format(message.chat.first_name))

@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, '/get - get your music\n/set [vk_id] - set your VK ID')

@bot.message_handler(commands=['set'])
def handle_start_help(message):
    global current_user
    current_user.vk_id = message.text[5:]
    bot.send_message(message.chat.id, "Your vk_id = {0}".format(current_user.vk_id ))

@bot.message_handler(commands=['get'])
def handle_start_help(message):
    global current_user
    if current_user.vk_id == 0:
        bot.send_message(message.chat.id, "Set your vk_id, please!")
    else:
        # loader = AudioLoader(current_user.vk_id, 5)
        # file = loader.get_audio()
        bot.send_message(message.chat.id, "Sorry")

if __name__ == '__main__':
     bot.polling(none_stop=True)