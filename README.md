# Сферум бот

## Использование

##  Качаем код и заполянем нужные данные

```
git clone https://github.com/dzenbots/sferum_delivery.git
cd sferum_delivery
```

Скопировать файл <kbd>.env.dist</kbd> в <kbd>.env</kbd> (или просто переименовать) и заполнить нужные поля

[Sferum](https://web.vk.me/) >> <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> >> Application >> Storage >> Cookies >> ```https://web.vk.me```
After that you must see **table** with all cookies from this site!
in filter put ```remixdsid``` and copy data from **value** column.

В файле main.py Ввести текст вместо "Тестовое сообщение из бота"

## Настраиваем окружение

```
python3 -m venv ./venv
source ./venv/bin/activate (для Win venv\Scripts\activate.bat)
pip install -r requirements.txt
```

## Запускаем

```
python3 start.py
```
