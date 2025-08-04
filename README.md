# Vertical Animation Player

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Веб-приложение для отображения анимаций на вертикальных мониторах с управлением через HTTP API.

## Возможности

- 🖥️ Полноэкранный режим для вертикальных мониторов
- 🔄 Автоматическая смена анимаций с настраиваемым таймером
- 🎛️ Управление через HTTP API
- ⚡ Обновление без перезагрузки страницы
- 📂 Простое добавление анимаций - достаточно HTML-файлов

## Установка

### Требования
- Python 3.7+
- Менеджер пакетов pip

### Установка
1. Клонируйте репозиторий:
```git clone https://github.com/ваш-пользователь/vertical-animation-player.git
cd vertical-animation-player```

2. Установите зависимости:
```pip install -r requirements.txt```

Использование
Поместите HTML-анимации в папку static/animations/

Запустите сервер:
```python app.py```
Откройте в браузере: http://localhost:5000

HTTP API
Метод	Эндпоинт	Описание
GET	/current-animation	Получить текущую анимацию
GET	/list-animations	Список всех анимаций
POST	/set-animation	Установить конкретную анимацию
GET	/next	Следующая анимация
GET	/previous	Предыдущая анимация
GET	/enable-timer	Включить автопереключение
GET	/disable-timer	Выключить автопереключение
GET	/set-timer?minutes=X	Установить интервал (в минутах)
Структура проекта
text
vertical-animation-player/
├── static/
│   └── animations/          # Папка для анимаций
├── templates/
│   └── player.html          # Шаблон плеера
├── app.py                   # Основное приложение
├── requirements.txt         # Зависимости
└── README.md                # Документация
Развертывание
Для production-использования рекомендуется:

Использовать WSGI-сервер (Gunicorn)

Настроить Nginx в качестве прокси

Запускать как systemd-сервис

Пример команды для Gunicorn:

bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Лицензия
Проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.


Версия: 1.0.0
