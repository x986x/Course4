import json
import os
from abc import ABC, abstractmethod

import requests
from dotenv import load_dotenv


class Api(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, word: object):
        pass


class HhApi(Api):

    def __init__(self, count):
        """
        Конструктор с входным параметром количество вакансий, который устанавливает параметры для гет-запросов
        """
        self.params = {
            'per_page': count,
            'area': 1,
            'page': 1
        }
        self.url = 'https://api.hh.ru/vacancies/'

    def get_vacancies(self, words):
        """
        Метод получения вакансий и преобразования их из json в словари
        """
        self.params['text'] = words
        r = requests.get(self.url, params=self.params)
        vacancies = json.loads(r.text)["items"]
        return vacancies


class SuperJobApi(Api):

    def __init__(self, count):
        """
        Конструктор с входным параметром количества вакансий,
        который устанавливает параметры и заголовки для гет-запросов
        """
        load_dotenv()
        __api_token: str = "v3.r.137974254.b7b39d1128e3711fb7a995fd28aae83e611bbc10.1e8beb32e0541c2565eaa46bf3e7b0604800fc7b"
        self.headers = {
            "X-Api-App-Id": f"{__api_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.params = {
            'count': count,
            'page': 1,
            'town': 'Moscow'
        }
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, words):
        """
        Метод для получения вакансий и преобразования их из json в словари
        """
        self.params['keywords'] = words
        r = requests.get(self.url, params=self.params, headers=self.headers)

        try:
            vacancies = json.loads(r.text)['objects']
        except KeyError:
            print(r.text)
            vacancies = []

        return vacancies
