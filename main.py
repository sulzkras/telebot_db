
import telebot
from database import add_task, get_task, register_user, delete_task, status_task
bot = telebot.TeleBot("")


@bot.message_handler(commands = ["start"])
def start_handler(message):
	bot.send_message(chat_id = message.chat.id, text = "Бот запущен")
	bot.reply_to(message, "/start - Перезапустить бота,\n"
	                      "/register - Зарегестрироваться,\n"
	                      "/add_task - Добавить задачу,\n"
	                      "/list_task - Показать Список задач,\n"
	                      "/deletetask - Поставить номер задачи для ее удаления,\n"
	                      "/statustask - Поставить номер задачи для изменения ее статуса")


@bot.message_handler(commands = ["register"])
def register_handler(message):
	flag = register_user(message)
	bot.reply_to(message, flag)


@bot.message_handler(commands = ["deletetask"])
def deletetask_handler(message):
	flag = delete_task(message)
	bot.reply_to(message, flag)


@bot.message_handler(commands = ["add_task"])
def add_task_handler(message):
	flag = add_task(message)
	bot.reply_to(message, flag)


@bot.message_handler(commands = ["list_task"])
def get_tasks_handler(message):
	flag = get_task(message)
	bot.reply_to(message, flag)


@bot.message_handler(commands = ["statustask"])
def status_task_handler(message):
	flag = status_task(message)
	bot.reply_to(message, flag)


bot.set_my_commands([
	telebot.types.BotCommand("/start", "Перезапустить бота"),
	telebot.types.BotCommand("/register", "Зарегестрироваться"),
	telebot.types.BotCommand("/add_task", "Добавить задачу"),
	telebot.types.BotCommand("/list_task", "Показать Список"),
	telebot.types.BotCommand("/deletetask", "поставить номер задачи для ее удаления"),
	telebot.types.BotCommand("/statustask", "поставить номер задачи для изменения ее статуса"),
])

bot.polling()