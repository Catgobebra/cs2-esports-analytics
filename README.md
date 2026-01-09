# Система аналитической оценки для энтузиастов ставок на киберспорт CS2 
**Система аналитической оценки для энтузиастов ставок на киберспорт CS2** — веб-сервис, который помогает понять, кто победит в матче между двумя профессиональными командами.
На основе актуальной статистики с HLTV сервис рассчитывает вероятность победы каждой команды с помощью модели машинного обучения, показывает динамику рейтинга, сравнение по картам и ключевые показатели (win rate, K/D, maps played).
Идеально для фанатов, аналитиков и тех, кто хочет делать обоснованные прогнозы на турниры. 

## Технологии

* Backend: Python 3.10, Django 5.2
* Machine Learning: XGBoost
* Data processing: Pandas
* Frontend: Tailwind CSS, daisyUI (компоненты), HTMX (динамическое обновление контента), Chart.js (интерактивные графики)
* База данных: SQLite
* Деплой: PythonAnywhere

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![DaisyUI](https://img.shields.io/badge/daisyui-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white) 
![htmx](https://img.shields.io/badge/htmx-%233366CC.svg?style=for-the-badge&logo=htmx&logoColor=white) ![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white) 
![PythonAnywhere](https://img.shields.io/badge/pythonanywhere-%232F9FD7.svg?style=for-the-badge&logo=pythonanywhere&logoColor=151515)

## Скриншоты
**Главная страница — выбор команд**
<kbd>
<img width="1533" height="847" alt="image" src="https://github.com/user-attachments/assets/bf94a1ec-bc80-450c-bc6b-7669e2827b30" />
</kbd>
**Главная страница — результат анализа матча (ч1)**
<kbd>
<img width="1253" height="839" alt="image" src="https://github.com/user-attachments/assets/676b5cb6-5378-4bf9-b95a-9bec5ad25294" />
</kbd>
**Главная страница — результат анализа матча (ч2)**
<kbd>
<img width="1327" height="907" alt="image" src="https://github.com/user-attachments/assets/e93b82c3-e565-4368-8037-863eb8d7f438" />
</kbd>

## Как запустить проект локально
1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ваш-юзернейм/ваш-репо.git](https://github.com/ваш-юзернейм/ваш-репо.git)
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Выполните миграции:**
   ```bash
   python manage.py migrate
   ```
5. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```
6. **Откройте проект в браузере:**
   Перейдите по ссылке: http://127.0.0.1:8000/****
   ~~Приложение будет работать, но юд будет пустая. Т.к. нужно каждый раз объединять с новыми данными~~

## Ссылка на рабочий проект: https://catgo.pythonanywhere.com
