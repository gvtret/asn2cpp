# asn2cpp Setup

Этот проект использует **виртуальное окружение** (`.venv`) для изоляции зависимостей.

## Требования
- Python 3.8+
- pip

## Установка окружения

```bash
# Клонировать репозиторий
git clone https://github.com/gvtret/asn2cpp.git
cd yourproject

# Создать виртуальное окружение
python3 -m venv .venv

# Активировать окружение
# (Linux / macOS)
source .venv/bin/activate
# (Windows)
.venv\Scripts\activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt
```

## Добавление новых зависимостей

```bash
pip install <package_name>
# После установки обновить requirements.txt
pip freeze > requirements.txt
```

## Запуск проекта

```bash
python asn2cpp.py [ASN.1 file] [output folder]
```

## Деактивация окружения

```bash
deactivate
```

## Обновление зависимостей

```bash
pip freeze > requirements.txt
```

## Генерация `requirements.txt` из текущего окружения

```bash
pip freeze > requirements.txt
```

## Полезные команды

```bash
pip list
pip uninstall <package_name>
pip list --outdated
```
