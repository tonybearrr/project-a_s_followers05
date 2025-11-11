# 📖 Address Book Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/static/v1?label=tests&message=400%2B&color=brightgreen&logo=pytest)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Персональний помічник з адресною книгою та нотатками**

*Потужний CLI-застосунок для управління контактами, нотатками та днями народження*

[🚀 Початок роботи](#-швидкий-старт) • [📋 Команди](#-доступні-команди) • [🏗️ Архітектура](#️-архітектура) • [🧪 Тестування](#-тестування)

</div>

---

## 📑 Зміст

- [Опис](#-опис)
- [Швидкий старт](#-швидкий-старт)
- [Доступні команди](#-доступні-команди)
- [Приклади використання](#-приклади-використання)
- [Архітектура](#️-архітектура)
- [Тестування](#-тестування)
- [Команда](#-команда)
- [Ліцензія](#-ліцензія)

---

## 📝 Опис

**Address Book Assistant** — це інтерактивний командний інтерфейс для управління персональною адресною книгою та нотатками. Застосунок дозволяє зберігати контакти з номерами телефонів, email-адресами, адресами та днями народження, а також створювати та керувати нотатками з тегами.

### 🎯 Основні Можливості

| Функція | Опис |
|---------|------|
| 📞 **Управління контактами** | Додавання, редагування, видалення контактів з валідацією номерів телефонів |
| 📧 **Email адреси** | Збереження та управління email-адресами з валідацією формату |
| 🎂 **Дні народження** | Збереження дат народження та нагадування про майбутні святкування |
| 📍 **Адреси** | Збереження та управління адресами контактів |
| 📝 **Нотатки** | Створення нотаток з тегами, сортування та пошук |
| 🔍 **Пошук** | Швидкий пошук контактів та нотаток за різними критеріями |
| 💾 **Збереження даних** | Автоматичне збереження в pickle файли |
| 🎨 **Кольоровий вивід** | Красиве форматування з використанням colorama та tabulate |
| 📊 **Статистика** | Комплексна статистика контактів, нотаток та днів народження |

### 🎨 Візуальні особливості

- Кольорове підсвічування команд та результатів `colorama`
- Форматування таблиць через `tabulate`
- Інтерактивні підказки та допомога
- Емодзі для кращої візуалізації

---

## 🚀 Швидкий старт

### Вимоги

- Python 3.11 або вище
- pip (менеджер пакетів Python)

### Залежності

Проект використовує наступні бібліотеки (вказані в `requirements.txt`):

```
pytest==8.4.2      # Тестування
flake8==7.1.1      # Лінтер коду
colorama==0.4.6    # Кольоровий вивід
tabulate==0.9.0    # Форматування таблиць
```

### Крок за кроком

1. **Переконайтеся, що у вас встановлений Python 3.11+:**
```bash
python3 --version
```

2. **Клонуйте репозиторій:**
```bash
git clone https://github.com/tonybearrr/project-a_s_followers05.git
cd project-a_s_followers05
```

3. **Створіть та активуйте віртуальне середовище:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# або
.venv\Scripts\activate  # Windows
```

4. **Встановіть залежності:**
```bash
pip install -r requirements.txt
```

5. **Запустіть застосунок:**
```bash
python main.py
```

---
## 📋 Доступні команди

### Контакти

| Команда | Опис | Приклад |
|---------|------|---------|
| `add` | Додати контакт | `add "John Doe" 1234567890` |
| `change` | Оновити телефон | `change "John Doe" 1234567890 0987654321` |
| `phone` | Показати телефон | `phone "John Doe"` |
| `all` | Показати всі контакти | `all` |
| `search` | Пошук контактів | `search John` |
| `delete` | Видалити контакт | `delete "John Doe"` |

### Email

| Команда | Опис | Приклад |
|---------|------|---------|
| `add-email` | Додати email | `add-email "John Doe" john@example.com` |
| `show-email` | Показати email | `show-email "John Doe"` |
| `delete-email` | Видалити email | `delete-email "John Doe"` |

### Дні народження

| Команда | Опис | Приклад |
|---------|------|---------|
| `add-birthday` | Додати день народження | `add-birthday "John Doe" 15.03.1990` |
| `show-birthday` | Показати день народження | `show-birthday "John Doe"` |
| `birthdays` | Майбутні дні народження | `birthdays 7` |

### Адреси

| Команда | Опис | Приклад |
|---------|------|---------|
| `add-address` | Додати адресу | `add-address "John Doe" "123 Main St"` |
| `change-address` | Змінити адресу | `change-address "John Doe" "456 New Ave"` |
| `remove-address` | Видалити адресу | `remove-address "John Doe"` |

### Нотатки

| Команда | Опис | Приклад |
|---------|------|---------|
| `add-note` | Додати нотатку | `add-note "Call John" work` |
| `list-notes` | Список нотаток | `list-notes created d` |
| `search-notes` | Пошук нотаток | `search-notes meeting` |
| `search-tags` | Пошук за тегами | `search-tags work important` |
| `edit-note` | Редагувати нотатку | `edit-note 1 "New text" tag` |
| `delete-note` | Видалити нотатку | `delete-note 1` |

### Система

| Команда | Опис | Приклад |
|---------|------|---------|
| `stats` | Статистика | `stats` |
| `help` / `?` | Допомога | `help` або `help contacts` |
| `hello` | Привітання | `hello` |
| `exit` / `close` | Вихід | `exit` |

### Сортування нотаток

Команда `list-notes` підтримує сортування:

```bash
list-notes created a    # За датою створення (зростання)
list-notes created d    # За датою створення (спадання)
list-notes updated a    # За датою оновлення (зростання)
list-notes updated d    # За датою оновлення (спадання)
list-notes text a       # За текстом (алфавітно)
list-notes text d       # За текстом (зворотно)
list-notes tags a       # За тегами (алфавітно)
list-notes tags d       # За тегами (зворотно)
```


## 📝 Приклади використання

### Приклад 1: Створення контакту

```bash
➜ Enter a command: add "Alice Smith" 0501234567
Contact 'Alice Smith' with phone '0501234567' added successfully.

➜ Enter a command: add-email "Alice Smith" alice@example.com
Email 'alice@example.com' added for contact 'Alice Smith'.

➜ Enter a command: add-birthday "Alice Smith" 20.05.1985
Birthday added for Alice Smith: 20.05.1985

➜ Enter a command: add-address "Alice Smith" "123 Main Street, Kyiv"
Address added for Alice Smith: 123 Main Street, Kyiv
```

### Приклад 2: Перегляд контактів

```bash
➜ Enter a command: all
╭─────────────┬────────────┬──────────────────────┬────────────┬──────────────────────╮
│ Name        │ Phones     │ Email                │ Birthday   │ Address              │
├─────────────┼────────────┼──────────────────────┼────────────┼──────────────────────┤
│ Alice Smith │ 0501234567 │ alice@example.com    │ 20.05.1985 │ 123 Main Street, Kyiv│
╰─────────────┴────────────┴──────────────────────┴────────────┴──────────────────────╯
```

### Приклад 3: Робота з нотатками

```bash
➜ Enter a command: add-note "Call Alice tomorrow" work urgent
Note `#`1 added with tags: work, urgent.

➜ Enter a command: list-notes
╭─────┬──────────────────────┬─────────────────┬──────────────────┬──────────────────╮
│   # │ Text                 │ Tags            │ Created          │ Updated          │
├─────┼──────────────────────┼─────────────────┼──────────────────┼──────────────────┤
│   1 │ Call Alice tomorrow  │ work, urgent    │ 2025-01-15 10:30 │ 2025-01-15 10:30 │
╰─────┴──────────────────────┴─────────────────┴──────────────────┴──────────────────╯
```

### Приклад 4: Статистика

```bash
➜ Enter a command: stats
══════════════════════════════════════════════════════════════════════
                         📊 STATISTICS
══════════════════════════════════════════════════════════════════════

📇 Contacts: 5
📝 Notes: 10
🔝 TOP 3 TAGS:
    1. work (4 notes)
    2. urgent (3 notes)
    3. home (1 notes)

🎂 Upcoming Birthdays (next 10 days):
  🎉 Alice Smith - 20.05 (TODAY!) - will be 40 years old
  🎁 Bob Wilson - 21.05 (Tomorrow) - will be 35 years old

══════════════════════════════════════════════════════════════════════
```

---
---

## 🏗️ Архітектура

### Структура проекту

```
project-a_s_followers05/
├── main.py                 # Точка входу застосунку
├── core/                   # Основна логіка
│   ├── commands.py         # Визначення команд
│   ├── handlers.py         # Обробники команд
│   └── decorators.py       # Декоратори (обробка помилок)
├── models/                 # Моделі даних
│   ├── record.py           # Клас Record (контакт)
│   ├── address_book.py     # Клас AddressBook
│   ├── note.py             # Клас Note
│   ├── notebook.py         # Клас NoteBook
│   ├── name.py             # Клас Name
│   ├── phone.py            # Клас Phone
│   ├── email.py            # Клас Email
│   ├── birthday.py         # Клас Birthday
│   ├── address.py          # Клас Address
│   └── field.py            # Базовий клас Field
├── utils/                  # Утиліти
│   ├── parsers.py          # Парсинг вводу
│   ├── help_formatter.py   # Форматування допомоги
│   ├── table_formatters.py # Форматування таблиць
│   └── confirmations.py    # Підтвердження дій
├── storage/                # Збереження даних
│   └── file_storage.py     # Робота з файлами (pickle)
├── tests/                  # Тести
│   ├── core/               # Тести core модулів
│   ├── models/             # Тести моделей
│   ├── storage/            # Тести storage
│   └── utils/              # Тести утиліт
├── requirements.txt        # Залежності
├── pytest.ini              # Конфігурація pytest
└── README.md               # Документація
```

### Діаграма класів

```
Field (базовий клас)
├── Name
├── Phone
├── Email
├── Birthday
└── Address

Record
├── name: Name
├── phones: List[Phone]
├── email: Email (optional)
├── birthday: Birthday (optional)
└── address: Address (optional)

AddressBook
└── data: Dict[str, Record]

Note
├── text: str
├── tags: List[str]
├── created_at: datetime
└── updated_at: datetime

NoteBook
└── notes: Dict[str, Note]
```

### Шари архітектури

1. **User Interface Layer** — `main.py`, CLI інтерфейс
2. **Core Layer** — `core/` (команди, обробники, декоратори)
3. **Models Layer** — `models/` (структури даних)
4. **Utils Layer** — `utils/` (парсери, форматування)
5. **Storage Layer** — `storage/` (персистентність)

### Особливості реалізації

- **ООП** — об'єктно-орієнтований підхід
- **Enum** — типізація команд
- **Декоратори** — обробка помилок
- **Pickle** — серіалізація даних
- **Валідація** — перевірка вхідних даних

---

## 🧪 Тестування

### Запуск тестів

```bash
# Всі тести
pytest

# З покриттям
pytest --cov=.

# З виводом
pytest -v

# Конкретний тест
pytest tests/models/test_record.py

# Конкретний тестовий метод
pytest tests/models/test_record.py::TestRecord::test_add_phone
```

### Статистика тестів

- **400+ тестів** для всіх функцій
- **Повне покриття** всіх модулів
- **Валідація даних** та обробка помилок
- **Інтеграційні тести** для основних сценаріїв

### Структура тестів

```
tests/
├── core/
│   ├── test_handlers.py      # Тести обробників команд
│   └── test_decorators.py    # Тести декораторів
├── models/
│   ├── test_record.py        # Тести Record
│   ├── test_address_book.py  # Тести AddressBook
│   ├── test_note.py          # Тести Note
│   └── ...                   # Інші моделі
├── storage/
│   └── test_file_storage.py  # Тести збереження
└── utils/
    └── test_parsers.py       # Тести парсерів
```
---

## 👥 Команда

Проект розроблено командою **"Послідовники Степана Андрійовича"**:

- **Еліна Сітайло** — Розробник
- **Наталя Дзюблюк** — Scrum Master / Розробник
- **Тарас Сітайло** — Розробник
- **Богдан Кужель** — Розробник
- **Антон Булавенко** — Team Lead / Розробник

---

## 📄 Ліцензія

Цей проект розповсюджується під ліцензією MIT. Детальніше дивіться у файлі `LICENSE`.

---

## 🔗 Посилання

- **GitHub**: [https://github.com/tonybearrr/project-a_s_followers05](https://github.com/tonybearrr/project-a_s_followers05)
- **Email**: [tonybear.bb@gmail.com](mailto:tonybear.bb@gmail.com)

---

<div align="center">

**Зроблено з ❤️ командою "Послідовники Степана Андрійовича"**

*© 2025 Address Book Assistant. Всі права захищені.*

</div>
