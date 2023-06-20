# weather-bot

## Перед коммитом

``` bash
pipenv shell
pydocstyle
flake8
```

## Запуск бота

``` bash
pipenv run python src/main.py 
```

## Постановка решаемой задачи

Разработать Telegram бота, который позволяет пользователям получать информацию о погоде для любого города или
местоположения.
Бот получает текущие данные о погоде для указанного места, используя, например, `OpenWeatherMap`, а в ответ
отправляет сообщение с текущими погодными условиями, включая температуру, влажность, скорость ветра и описание погоды.

## Описание предполагаемых инструментов решения

Основными инструментами являются Python библиотека `python-telegram-bot` для создания Telegram бота, а также
Python обёртка над `OpenWeatherMap` API, `PyOWM`.

## Макет интерфейса

Бот имеет текстовый интерфейс и взаимодействует с пользователем через Telegram.
Пользователь отправляет запрос на получение информации о погоде в виде сообщения боту,
который обрабатывает его и отправляет ответное сообщение с информацией о погоде.

Бот предоставляет информации о погоде в том числе через кнопочный интерфейс:

![image](https://raw.githubusercontent.com/Sidl419/weather-bot/master/.github/images/buttons.jpg)

Доступна функция получения прогноза погоды на ближайшие три дня, отправляемой в виде фотографии. Пользователь может вводить город с клавиатуры, либо с помощью выбора по кнопке.

![image](https://raw.githubusercontent.com/Sidl419/weather-bot/master/.github/images/forecast.jpg)

Помимо основной информации о погоде бот выдаёт эмодзи-визуализацию с дополнительным интересным фактом о полученных данных:

![image](https://raw.githubusercontent.com/Sidl419/weather-bot/master/.github/images/message.jpg)

Также с введенной системой перевода бот может выдавать ответы на запросы как на английском, так и на русском языках.

![image](https://raw.githubusercontent.com/Sidl419/weather-bot/master/.github/images/ru_lang.jpg)

Примеры команд для бота:

1. `/start`: начало работы с ботом;

2. `/help`: отображение списка доступных команд и их описание;

3. `/weather <город/метка>`: текущая погода для указанного города или метки;

4. `/get5`: прогноз погоды в виде кнопочного интерфейса с дополнительной визуализацией;

5. `/getw`: прогноз погоды на три дня вперёд, отправляемой в виде фотографии;

6. `/cancel`: завершить взаимодействие;


## Автоматическая документация

Автоматическая документация проекта доступна по [ссылке](https://sidl419.github.io/weather-bot).
