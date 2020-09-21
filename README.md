# LoggerBotLoggingServer
Сервер, который принимает логи от клиента и записывает их в базу данных
## Структура
Проект использует Quart - асинхронную версию фреймворка Flask, базу данных MySQL.

Клиент в данном случае - является [logger](https://github.com/den-bibik/LoggerBotLogging),
его можно поставить из https://github.com/den-bibik/LoggerBotLogging

![Schema](static/schema.png "Схема")

Сервер получает логи через api /send_logs в таком формате:

body:
```
{
  "data": {
    "user": "username",
    "pid": 1,
    "p_name": "process name",
    "post_time": "2020-05-05T12:22:22+00:00",
    "logs": [
      {
        "level": "error",
        "msg": "log message",
        "event_at" : "2020-05-05T12:22:22+00:00",
        "p_description": "process_user_description"
      },
      {
        "level": "warning",
        "msg": "other log message",
        "event_at" : "2020-05-06T12:22:22+00:00",
        "p_description": "process_user_description"
      }
      ...
    ]
  }
}
```
**logs** - в данном случае массив из логов пользователя, которые необходимо записать в базу данных

headers:
```
'Content-Type': 'application/json'
'X-User-Token': 'a5amka921jkmakguasl1kna9u6sl1241'
```
**X-User-Token** - токен захешированный в md5, по которому происходит аутентификация клиента

## Принцип работы
Сервер получает запрос от клиента, проверяет пару (user, X-User-Token) на наличие в таблице users.
Если пользователь с данной парой существует, то добавляем логи в таблицу user_logs, иначе возвращаем пользователю 403

Сервер отдает такие ответы:

- 200: `{"code": 200, "message": "Logs added successfully"}` - Логи успешно были добавлены в таблицу user_logs
- 400: `{"code": 400, "message": "BadRequest"}` - Был получен некорректный запрос
- 403: `{"code": 403, "message": "Forbidden"}` - Клиент не прошел аутентификацию
- 500: `{"code": 500, "message": "InternalServerError"}` - Внутренняя ошибка сервера

## Сборка и использование
### Установка
Ставим виртуальное окружение, например
virtualenv:`pip3 install virtualenv`
Клонируем репозиторий:

```
git clone https://github.com/WesBAn/LoggerBotLoggingServer
```
Устанавливаем окружение и зависимости:
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Для запуска необходимо поднять сервер MySQL
### Настройка сервера и запуск
Логин и пароль для MySQL можно вынести в переменные среды, пример:
```
export LOGGER_DB_USER=user
export LOGGER_DB_PASSWORD=password
```
IP сервера и порт нужно записать в конфиг
>bot_logging_server/config/quart_config.py

**Запуск:**
```
python3 app.py
```

### Запуск сервера без настройки
Пример для запуска сервера без предварительной настройки (см. выше):
```
python3 app.py --host=localhost --port=5000 --user=user --password=password
```
Где:
- `--host` - ip сервера
- `--port` - port сервера
- `--user` - MySQL логин
- `--password` - MySQL пароль

### Документация
```
source venv/bin/activate
export PYTHONPATH=`pwd`
cd bot_logging_server
python3 -m pydoc -p port
```
По полученной ссылке можно посмотреть документацию

### Тестирование
Для тестирования используется стандартный фреймворк pytest
```
source venv/bin/activate
export PYTHONPATH=`pwd`
pytest
```

### Сборка колеса
```
source venv/bin/activate
python3 setup.py bdist_wheel
```
