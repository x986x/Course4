import json
import os
from src.vacancy import Vacancy

FILE = 'vacancies.json'


class JsonAgent:

    @staticmethod
    def check_for_repeat(vacancy: Vacancy):
        """
        Метод для проверки на уже существующие вакансии в файле json
        """
        try:
            with open(FILE, 'r', encoding='utf-8') as f:
                vacancies = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            vacancies = []  # Если файл не существует или пуст, создаем пустой список вакансий.

        for v in vacancies:
            if v['title'] == vacancy.title and v['url'] == vacancy.url and \
                    v['pay'] == vacancy.pay and v['requirement'] == vacancy.requirement:
                return False

        return True

    @staticmethod
    def add_vacancy(vacancy: Vacancy):
        """
        Метод для добавления вакансии в файл json
        """
        if not os.path.exists(FILE):
            with open(FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
                print("Файл vacancies.json был создан.")

        print("Попытка добавить вакансию")
        if JsonAgent.check_for_repeat(vacancy):
            with open(FILE, 'r', encoding='utf-8') as f:
                try:
                    vacancies = json.load(f)
                except json.JSONDecodeError:
                    print("Файл vacancies.json поврежден. Создаю новый файл.")
                    with open(FILE, 'w', encoding='utf-8') as new_f:
                        json.dump([], new_f)
                    vacancies = []

            vacancies.append(vacancy.to_json())
            with open(FILE, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False)
            print("Вакансия успешно добавлена")
            return True
        else:
            print("Произошла ошибка при добавлении вакансии")
            return False

    @staticmethod
    def delete_vacancy_by_title(title):
        """
        Метод, который удаляет вакансию из файла по её названию.
        Возвращает true если вакансия найдена и удалена, иначе False.
        """
        try:
            with open(FILE, 'r', encoding='utf-8') as f:
                vacancies = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Произошла ошибка при загрузке вакансий.")
            return False

        f = False
        for vacancy in vacancies:
            if vacancy['title'] == title:
                vacancies.remove(vacancy)
                f = True
                break
        if f:
            with open(FILE, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False)
            return True
        else:
            return False

    @staticmethod
    def show_vacancies_title():
        """
        Метод, который выводит в консоль названия всех вакансий в файле
        """
        try:
            with open(FILE, 'r', encoding='utf-8') as f:
                vacancies = json.load(f)
            if not vacancies:
                print("Файл с вакансиями пуст.")
            else:
                for vacancy in vacancies:
                    print(vacancy['title'])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Произошла ошибка при загрузке вакансий.")

    @staticmethod
    def clear_json():
        """
        Метод, который очищает json файл
        """
        with open(FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)

    @staticmethod
    def show_info_by_title():
        """
        Метод, который выводит в консоль информацию о найденной по названию вакансии
        """
        with open(FILE, 'r', encoding='utf-8') as f:
            vacancies = Vacancy.all_from_json(f)
        for vacancy in vacancies:
            if vacancy.title == 'title':
                vacancy.show_info()
                break
