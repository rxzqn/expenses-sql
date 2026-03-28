import sqlite3
from datetime import date

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        category TEXT,
        amount REAL,
        date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS incomes (
        id INTEGER PRIMARY KEY,
        category TEXT,
        amount REAL,
        date TEXT
    )
''')
def add_expense(category, amount):
    cursor.execute('''
        INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)
    ''', (category, amount, str(date.today())))
    conn.commit()

def add_income(category, amount):
    cursor.execute('''
    INSERT INTO incomes (category, amount, date) VALUES (?, ?, ?)
    ''', (category, amount, str(date.today())))
    conn.commit()

def get_balance():
    cursor.execute('SELECT SUM(amount) FROM incomes')
    total_income = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(amount) FROM expenses')
    total_expense = cursor.fetchone()[0] or 0

    return total_income - total_expense

def show_expenses():
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')

    rows = cursor.fetchall()
    for row in rows:
        print(f' {row[0]}: {row[1]}')

while True:
    print('=== MoneyBase SQL Edition===')
    print('1.Добавить расход')
    print('2.Добавить доход')
    print('3.Посмотреть баланс')
    print('4.Показать расходы по категориям')
    print('5.Выйти')
    choice = input('Выбери действие: ')
    if choice == '1':
        category = input("Категория (еда/транспорт/учёба): ")
        amount = int(input("Сумма: "))
        add_expense(category, amount)
    elif choice == '2':
        category = input("Источник дохода (зарплата/фриланс/подарок): ")
        amount = int(input("Сумма: "))
        add_income(category, amount)
    elif choice == '3':
        print(f'Текущий баланс: {get_balance()}')
    elif choice == '4':
        show_expenses()
    elif choice == '5':
        break
    else:
        print("Некорректный ввод")
