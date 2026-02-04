"""Основной скрипт запуска приложения"""


from database.database import Database


def main():
    print("Скрипт запущен")
    print("Инициализация базы")
    db = Database("testing.db")
    print("Заполнение базы тестовыми значениями")
    db.create_testing_data()
    
    

if __name__ == "__main__":
    main()