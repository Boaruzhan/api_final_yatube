# API проект YATUBE 

## Как запустить проект:
### Клонировать репозиторий и перейти в него в командной строке:
``` git clone git@github.com:Boaruzhan/api_final_yatube.git```
``` cd yatube_api```
### Cоздать и активировать виртуальное окружение:
``` python -m venv venv ```
``` source /venv/scripts/activate ```

### Установить зависимости из файла requirements.txt:
``` python -m pip install --upgrade pip ```
``` pip install -r requirements.txt ```
 ### Выполнить миграции:
 ``` python manage.py makemigrations ```
 ``` python manage.py migrate ```
 ### Запустить проект:
 ``` python manage.py runserver ```
### Документация проекта доступна по ссылке  
``` http://127.0.0.1:8000/redoc/ ```
 # Автор проекта: [Иосиф Улинец ](https://github.com/Boaruzhan)