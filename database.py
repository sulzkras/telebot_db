import sqlite3

connect = sqlite3.connect('database.db') # Создает подключенике к базе данных
cursor = connect.cursor()

create_tabl_task = """
CREATE TABLE IF NOT EXISTS tasks
	(id INTEGER PRIMARY KEY,
	user_id INTEGER,
	task TEXT,
	done BOOLEAN)
"""
create_tabl_user = """
CREATE TABLE IF NOT EXISTS users
	(id INTEGER PRIMARY KEY,
	name TEXT,
	chat_id INTEGER)
"""
cursor.execute(create_tabl_task) # Выполняет sql запрос на создание баззы даннных
cursor.execute(create_tabl_user)

connect.commit() # Сохраняет изменения в базе данных

#Регистрация пользователя
def register_user(message):
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	user = (message.from_user.first_name, message.from_user.id,)
	cursor.execute("INSERT INTO users (name, chat_id) VALUES (?, ?)", user)
	connect.commit()
	connect.close()
	return f"Вы Зарегистрированы, {user[0]}!"


#Удаление задачи
def delete_task(message):
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	chat_id = (message.from_user.id,)
	cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
	user = cursor.fetchone()
	if user is None:
		return "Вы не зарегестрированы!"
	else:
		task_id = message.text.split("/deletetask")[1]
		if len(task_id) != 0:
			task_id = (int(task_id),)
			user = (int(user[0]),)
			cursor.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", task_id + user)
			task = cursor.fetchone()
			if task is None:
				return "Такой записи нет"
			else:
				cursor.execute("DELETE FROM tasks WHERE id=?", task_id)
				connect.commit()
		else:
			return "Вы должны указать номер ID задачи, которую нужно удалить"
			
		connect.close()
	return f"Задача удалена {task_id}"


#добовление задачи
def add_task(message):
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	chat_id = (message.from_user.id,)
	cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
	user = cursor.fetchone()
	if user is None:
		# Если пользователя нет в базе данных
		return "Вы не зарегстрированы"
	else:
		task = message.text.split("/add_task")[1]
		if len(task) != 0:
			task_data = (user[0], task, False)
			cursor.execute("INSERT INTO tasks (user_id, task, done) VALUES (?, ?, ?)", task_data)
			connect.commit()
		else:
			return "Пустая задача не допускается"
	connect.close()
	return "Ваша задача добавленна"

#Показ пользователю список задач
def get_task(message):
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	chat_id = (message.chat.id,)
	cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
	user = cursor.fetchone()
	if user is None:
		return "Вы не зарегистрированы"
	else:
		user = (int(user[0]),)
		cursor.execute("SELECT * FROM tasks WHERE user_id=?", user)
		tasks = cursor.fetchall()
		if tasks:
			task = '\n'
			for i in tasks:
				# task += f"ID записи: {i[0]}\nОписание задачи: {i[2]}\nСостояние задачи: {False if i[3] == 0 else True}\n\n"
				if i[3] == 0:
					task += f"ID записи: {i[0]}\nОписание задачи: {i[2]}\nСостояние задачи: Не выполнена\n\n"
				else:
					task += f"ID записи: {i[0]}\nОписание задачи: {i[2]}\nСостояние задачи: Выполнена\n\n"
		else:
			return "У вас нет задач"
	connect.close()
	return task

#Изменение статуса задачи с False на True и обратно
def status_task(message):
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	chat_id = (message.from_user.id,)
	cursor.execute("SELECT * FROM users WHERE chat_id=?", chat_id)
	user = cursor.fetchone()
	if user is None:
		return "Вы не заригистрированы"
	else:
		task_id = message.text.split("/statustask")[1]
		if len(task_id) != 0:
			task_id = (int(task_id),)
			user = (int(user[0]),)
			cursor.execute("SELECT * FROM tasks WHERE id=? and user_id=?", task_id + user)
			task = cursor.fetchone()
			if task is None:
				return "Такой записи нет"
			else:
				cursor.execute("SELECT done FROM tasks WHERE id=?", task_id)
				task = cursor.fetchone()
				if task[0] == 0:
					cursor.execute("UPDATE tasks SET done=TRUE WHERE id=?", task_id)
					connect.commit()
					connect.close()
				else:
					cursor.execute("UPDATE tasks SET done=FALSE WHERE id=?", task_id)
					connect.commit()
					connect.close()
		else:
			return "Вы должны указать номер ID задачи, статус которой нужно изменить"
		connect.close()
	# return "Запись обновлена"
	if task[0] == 0:
		return f'Запись обновлена, текущий статус задачи - "Выполнена"'
	else:
		return f'Запись обновлена, текущий статус задачи - "Не выполнена"'
	
