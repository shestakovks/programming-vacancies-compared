import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif not salary_from:
        return salary_to * 0.8
    else:
        return salary_from * 1.2


def predict_rub_salary_hh(vacancy):
    salary_data = vacancy['salary']
    if salary_data is None or salary_data['currency'] != 'RUR':
        return None
    else:
        return predict_rub_salary(salary_data['from'], salary_data['to'])


def download_data_hh(url, params, verbose=True):
    page = 0
    pages = 1
    data = []
    while page < pages:
        if verbose:
            print(f'Downloading page {page}')
        params['page'] = page
        page_data = requests.get(url, params).json()
        pages = page_data['pages']
        page += 1
        data.append(page_data)
    return data


def get_statistics_hh(prog_langs, verbose=True):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 1,  # Moscow
        'period': 30,  # Last month
        'text': '',
    }

    vacancies_info = {}
    for prog_lang in prog_langs:
        params['text'] = f'name:Программист {prog_lang}'
        if verbose:
            print(prog_lang)
        vacancies_data = download_data_hh(url, params, verbose=verbose)

        total_salary = 0
        average_salary = 0
        vacancies_processed = 0
        vacancies_found = vacancies_data[-1]['found']
        vacancies = [item for sublist in vacancies_data
                     for item in sublist['items']]
        for vacancy in vacancies:
            avg_salary = predict_rub_salary_hh(vacancy)
            if avg_salary is not None:
                vacancies_processed += 1
                total_salary += avg_salary
        if total_salary != 0:
            average_salary = int(total_salary / vacancies_processed)

        vacancies_info[prog_lang] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }
    return vacancies_info


def predict_rub_salary_sj(vacancy):
    salary_currency = vacancy['currency']
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    salary = True if salary_from or salary_to else False

    if not salary or salary_currency != 'rub':
        return None
    else:
        return predict_rub_salary(salary_from, salary_to)


def download_data_sj(url, headers, params, verbose=True):
    page = 0
    is_not_last_page = True
    data = []
    while is_not_last_page:
        if verbose:
            print(f'Downloading page {page}')
        params['page'] = page
        page_data = requests.get(url, headers=headers, params=params).json()
        is_not_last_page = page_data['more']
        page += 1
        data.append(page_data)
    return data


def get_statistics_sj(secret_key, prog_langs, verbose=True):
    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'town': 4,  # Moscow
        'period': 30,  # Last month
        'catalogues': 48,  # Development, Programming
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'

    vacancies_info = {}
    for prog_lang in prog_langs:
        params['keyword'] = prog_lang
        if verbose:
            print(prog_lang)
        vacancies_data = download_data_sj(
            url, headers, params, verbose=verbose)

        total_salary = 0
        average_salary = 0
        vacancies_processed = 0
        vacancies_found = vacancies_data[-1]['total']
        vacancies = [item for sublist in vacancies_data
                     for item in sublist['objects']]
        for vacancy in vacancies:
            avg_salary = predict_rub_salary_sj(vacancy)
            if avg_salary is not None:
                vacancies_processed += 1
                total_salary += avg_salary
        if total_salary != 0:
            average_salary = int(total_salary / vacancies_processed)

        vacancies_info[prog_lang] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }
    return vacancies_info


def print_statistics(data, title):
    keys = [key for key in next(iter(data.values()))]
    table_data = [
        ['language', *keys],
    ]
    for k, v in data.items():
        table_data.append([k, *[v[key] for key in keys]])
    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == "__main__":
    load_dotenv()
    secret_key = os.getenv('SUPERJOB_APP_KEY')
    prog_langs = [
        'Python',
        'JavaScript',
        'Java',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Objective-C',
    ]
    lang_stat_hh = get_statistics_hh(prog_langs)
    lang_stat_sj = get_statistics_sj(secret_key, prog_langs)
    print_statistics(lang_stat_hh, 'HeadHunter Moscow')
    print_statistics(lang_stat_sj, 'SuperJob Moscow')
