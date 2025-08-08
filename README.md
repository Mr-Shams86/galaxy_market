
# 🚀 Galaxy Market

**Galaxy Market — это учебный e-commerce проект, предназначенный для демонстрации навыков работы с Django, базами данных, Docker и адаптивной вёрсткой. Реализована полноценная система интернет-магазина с возможностью размещения заказов, регистрации пользователей и панелью администратора.**

**Интернет-магазин оригинальных запчастей и аксессуаров для техники **Samsung**.  
**Платформа создана на Django с адаптивным дизайном, удобной корзиной и системой заказов.**

## ![Galaxy Market Screenshot]
## 📷 Скриншоты

### 🛍️ Каталог товаров
![Каталог](static/media/images/screenshots/catalog.png)

### ➕ Добавление товара
![Добавление товара](static/media/images/screenshots/add-product.png)

### 👤️ Профиль
![Отзывы](static/media/images/screenshots/profile.png)

### 📝️ Редактирование профиля
![Отзывы](static/media/images/screenshots/edit-profile.png)

### 📦 Оформление заказа
![Оформление заказа](static/media/images/screenshots/checkout.png)

### 🛒 Корзина
![Корзина](static/media/images/screenshots/cart.png)

### ✅ Подтверждение заказа
![Подтверждение](static/media/images/screenshots/confirm.png)


### 📦 Мои заказы
![История заказов](static/media/images/screenshots/my-orders.png)

### 💬 Отзывы пользователей
![Отзывы](static/media/images/screenshots/reviews.png)




## ⚙️ Технологии

- 🐍 **Python 3.10** — основной язык разработки
- 🌐 **Django 4.0.10** — веб-фреймворк (MTV архитектура)
- 🐘 **PostgreSQL 15** — СУБД для хранения данных
- 🐳 **Docker + Docker Compose** — контейнеризация проекта
- 🧠 **Redis 7** — хранилище состояний и кэш (через docker)
- 🎨 **Tailwind CSS** — утилитарный CSS-фреймворк
- 🔧 **PostCSS + Autoprefixer** — для сборки стилей Tailwind
- 💳 **Stripe** — интеграция онлайн-платежей
- 🖼️ **Pillow** — обработка изображений (аватары, каталог)
- 🔗 **django-widget-tweaks** — управление полями форм в шаблонах
- 🌍 **django-cors-headers** — обработка CORS-запросов (если будет frontend отдельно)
- 🔐 **python-dotenv** — загрузка переменных окружения из `.env`
- 🧰 **psycopg2-binary** — драйвер для PostgreSQL


## 🔥 Основной функционал

- 👤 Регистрация / авторизация пользователей
- 🛍️ Каталог товаров с категориями
- 🧺 Добавление товаров в корзину
- 💳 Оформление заказа (имя, телефон, адрес)
- 🔄 Просмотр и история заказов
- 📦 Профиль пользователя и продавца
- ✨ Отзывы, оплата и подтверждение
- 🧾 Адаптивный интерфейс под все устройства
- 🖼️ Загрузка и отображение аватара (с возможностью редактирования)

## 🛠️ Возможности административной панели

- Управление пользователями
- Управление товарами и категориями
- Просмотр и обработка заказов
- Работа с отзывами


## 🐳 Установка и запуск через Docker

```bash
# 1. Клонируй репозиторий
git clone https://github.com/your_username/galaxy-market.git
cd galaxy-market

# 2. Построй и запусти контейнеры
docker-compose up --build

# 3. Открой в браузере
http://localhost:8000

# 4. 🛠️ Начальная настройка (после запуска)

    📌 Примените миграции:

# 5. docker-compose exec web python manage.py migrate

    🔐 Создайте суперпользователя для доступа к админке:

# 6. docker-compose exec web python manage.py createsuperuser


# 7. 🔑 Админка доступна по адресу:
http://localhost:8000/admin/

```

---

## 🔗 Ссылки

- [Сайт проекта]

- [GitHub репозиторий](https://https://github.com/Mr-Shams86/galaxy_market)


## 📢 **Контакты**

👤 **Автор**

- ๛Samer Shams๖

- **Email**: sammertime763@gmail.com

- **Telegram**: [Mr_Shams_1986](https://t.me/Mr_Shams_1986)

---

---

## 🏢 **Структура проекта Galaxy Market**

```
📦 Проект
├── ⚙️ config/ — базовая конфигурация Django
│   ├── admin.py — административные настройки
│   ├── asgi.py — конфигурация ASGI
│   ├── init.py
│   ├── settings.py — основная конфигурация проекта
│   ├── urls.py — маршруты верхнего уровня
│   └── wsgi.py — конфигурация WSGI
│
├── 🐳 Docker & запускаемые файлы
│   ├── docker-compose.yml — настройка Docker-сервисов
│   ├── Dockerfile — инструкция сборки
│   ├── entrypoint.sh — скрипт запуска контейнера
│   └── manage.py — точка входа Django
│
├── 🖼 media/ — директория пользовательских файлов
│   ├── images/catalog/ — изображения товаров по категориям
│   │   ├── accessories, batteries, headphones, phones, etc.
│   └── profile_images/ — аватары пользователей
│
├── 🛒 orders/ — управление заказами
│   ├── admin.py — регистрация моделей в админке
│   ├── forms.py — формы для оформления заказа
│   ├── migrations/ — миграции БД
│   ├── models.py — модели Order и OrderItem
│   ├── urls.py — маршруты
│   └── views.py — логика отображения и обработки
│
├── 🛍 products/ — каталог товаров
│   ├── admin.py
│   ├── apps.py
│   ├── mixins.py — вспомогательные классы
│   ├── models/
│   │   └── product.py — модель товара
│   ├── migrations/
│   ├── tests.py — тесты для каталога
│   ├── urls.py
│   └── views.py
│
├── 💬 reviews/ — управление отзывами
│   ├── forms.py — форма добавления отзыва
│   ├── models.py — модель Review
│   ├── templatetags/
│   │   └── extras.py — кастомные шаблонные фильтры
│   ├── migrations/
│   ├── urls.py
│   └── views.py
│
├── 👤 users/ — аутентификация и профили
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models/
│   │   ├── user.py — кастомная модель пользователя
│   │   └── profile.py — профиль пользователя
│   ├── migrations/
│   ├── signals.py — авто-создание профиля при регистрации
│   ├── templatetags/
│   │   └── form_filters.py — кастомные фильтры
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── 📄 templates/ — HTML-шаблоны
│   ├── base.html — базовый шаблон
│   ├── navbar.html — верхняя панель
│   ├── orders/ — корзина, оформление, мои заказы
│   ├── products/ — каталог, детали, добавление, удаление
│   ├── reviews/ — мои отзывы
│   └── users/ — логин, регистрация, профиль, удаление
│
├── 🌐 static/ — статика проекта (CSS/картинки)
│   ├── img/ — изображения интерфейса
│   │   ├── background, default, logo
│   └── products/
│   ├── styles.css — кастомные стили
│   └── tailwind.css — стили Tailwind
│
├── 📦 requirements.txt — зависимости Python
├── 📦 package.json / package-lock.json — зависимости Node (Tailwind)
├── 🌀 tailwind.config.js / postcss.config.js — настройки TailwindCSS
├── 📄 README.md — описание проекта
├── 📄 structure.txt — сохранённая структура проекта
└── 📄 url_adress_in_my_Gadjet_Shop.txt — полезные ссылки/адреса

```
