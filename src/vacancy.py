import json

FILE = 'vacancies.json'


class Vacancy:

    def __init__(self, title, url, pay, requirement) -> None:
        """
        Конструктор, принимает название, ссылку, заработную плату, требования
        """
        self.title = title
        self.url = url
        self.pay = pay
        self.requirement = requirement

    def to_json(self):
        """
        Метод, который возвращает информацию о вакансии в виде словаря
        """
        return {
            'title': self.title,
            'url': self.url,
            'pay': self.pay,
            'requirement': self.requirement,
        }

    @classmethod
    def from_json(cls, params):
        """
        КлассМетод, который создает вакансию на основе словаря
        """
        return cls(params['title'], params['url'], params['pay'], params['requirement'])

    @classmethod
    def all_from_json(cls):
        """
        КлассМетод, который создает массив вакансий на основе информации из json файла
        """
        with open(FILE, 'r', encoding='utf-8') as f:
            vacancies = json.loads(f.read())
        output = []
        for vacancy in vacancies:
            tmp = Vacancy.from_json(vacancy)
            output.append(tmp)
        return output



    def show_info(self):
        """
        Метод, который выводит в консоль информацию о вакансии
        """
        print(self.title)
        print(self.url)
        print(f'Заработная плата {self.pay}')
        print(self.requirement)

    def __repr__(self) -> str:
        return f"{self.title}\n{self.pay}\n{self.url}\n{self.requirement}"


class VacancyAgent:

    @staticmethod
    def pars_super_job(vacancies):
        """
        Метод, который получает на вход словарь из superjob и возвращает массив Vacancy
        """
        output = []
        for vacancy in vacancies:
            if vacancy['payment_from'] is not None:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], vacancy['payment_from'], vacancy['candidat'])
            elif vacancy['payment_to'] is not None:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], vacancy['payment_to'], vacancy['candidat'])
            else:
                tmp = Vacancy(vacancy['profession'], vacancy['link'], '0', vacancy['candidat'])
            output.append(tmp)
        return output

    @staticmethod
    def pars_hh_ru(vacancies):
        """
        Метод, который получает на вход словарь из hh.ru и возвращает массив Vacancy
        """
        output = []
        for vacancy in vacancies:
            if vacancy['salary'] is not None:
                if vacancy['salary']['from'] is not None:
                    tmp = Vacancy(vacancy['name'], f'https://hh.ru/vacancy/{vacancy["id"]}', vacancy['salary']['from'],
                                  vacancy['snippet']['requirement'])
                else:
                    tmp = Vacancy(vacancy['name'], f'https://hh.ru/vacancy/{vacancy["id"]}', vacancy['salary']['to'],
                                  vacancy['snippet']['requirement'])
            else:
                tmp = Vacancy(vacancy['name'], f'https://hh.ru/vacancy/{vacancy["id"]}', "0",
                              vacancy['snippet']['requirement'])
            output.append(tmp)
        return output

    @staticmethod
    def filter_vacancies_by_keywords(vacancies: list, key_words=None):
        """
        Метод, который возвращает названия вакансий по заданным словам для поиска
        """
        if key_words is None:
            key_words = []
        output = []
        for vacancy in vacancies:
            title = [x.lower() for x in vacancy.title.split()]
            try:
                requiremets = [x.lower() for x in vacancy.requirement.split()]
            except AttributeError:
                requiremets = []
            for key_word in key_words:
                if key_word.lower() in title or key_word.lower() in requiremets:
                    output.append(vacancy.title)
                    break
        return output

    @staticmethod
    def filter_vacancies_by_salary(vacancies: list, sfrom, sto):
        """
        Метод, который возвращает названия вакансий по заданному диапазону заработной платы
        """
        output = []
        for vacancy in vacancies:
            try:
                if sfrom <= vacancy.pay <= sto:
                    output.append(vacancy.title)
            except (AttributeError, TypeError):
                pass
        return output
