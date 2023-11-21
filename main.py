from src.utils import *


if __name__ == "__main__":
    clear_json()
    load_vacancies_to_json()
    show_vacancies_by_title()
    delete_vacancy_by_title()
    get_vacancies_by_kwards()
    get_vacancies_by_salary()
    sort_vacancies_by_salary()
    show_top_n()
