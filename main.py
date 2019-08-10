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
    return predict_rub_salary(salary_data['from'], salary_data['to'])


def download_data_hh(url, params, verbose=True):
    page = 0
    pages = 1
    data = []
    while page < pages:
        if verbose:
            print(f'Downloading page {page}')
        params['page'] = page
        page_data = requests.get(url, params)
        page_data.raise_for_status()
        pages = page_data.json()['pages']
        page += 1
        data.append(page_data.json())
    print()
    return data


def get_statistics_hh(prog_lang, verbose=True):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 1,  # Moscow
        'period': 30,  # Last month
        'text': f'name:Программист {prog_lang}',
    }

    lang_stat = {}
    if verbose:
        print(f'{prog_lang} - HEADHUNTER')
    try:
        vacancies_pages = download_data_hh(url, params, verbose=verbose)

        vacancies = [vacancy for vacancies_page in vacancies_pages
                     for vacancy in vacancies_page['items']]
        avg_salaries = [predict_rub_salary_hh(vacancy)
                        for vacancy in vacancies
                        if predict_rub_salary_hh(vacancy) is not None]
        lang_stat['vacancies_found'] = vacancies_pages[-1]['found']
        lang_stat['vacancies_processed'] = len(avg_salaries)
        lang_stat['average_salary'] = int(
            sum(avg_salaries) / (len(avg_salaries) or 1))

    except requests.exceptions.HTTPError as e:
        print(f'Error occurred: "{e}"')
    return lang_stat


def predict_rub_salary_sj(vacancy):
    salary_currency = vacancy['currency']
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    salary = True if salary_from or salary_to else False

    if not salary or salary_currency != 'rub':
        return None
    return predict_rub_salary(salary_from, salary_to)


def download_data_sj(url, headers, params, verbose=True):
    page = 0
    is_not_last_page = True
    data = []
    while is_not_last_page:
        if verbose:
            print(f'Downloading page {page}')
        params['page'] = page
        page_data = requests.get(url, headers=headers, params=params)
        page_data.raise_for_status()
        is_not_last_page = page_data.json()['more']
        page += 1
        data.append(page_data.json())
    print()
    return data


def get_statistics_sj(secret_key, prog_lang, verbose=True):
    headers = {
        'X-Api-App-Id': secret_key,
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {
        'town': 4,  # Moscow
        'period': 30,  # Last month
        'catalogues': 48,  # Development, Programming
        'keyword': prog_lang,
    }

    lang_stat = {}
    if verbose:
        print(f'{prog_lang} - SUPERJOB')
    try:
        vacancies_pages = download_data_sj(
            url, headers, params, verbose=verbose)

        vacancies = [vacancy for vacancies_page in vacancies_pages
                     for vacancy in vacancies_page['objects']]
        avg_salaries = [predict_rub_salary_sj(vacancy)
                        for vacancy in vacancies
                        if predict_rub_salary_sj(vacancy) is not None]
        lang_stat['vacancies_found'] = vacancies_pages[-1]['total']
        lang_stat['vacancies_processed'] = len(avg_salaries)
        lang_stat['average_salary'] = int(
            sum(avg_salaries) / (len(avg_salaries) or 1))

    except requests.exceptions.HTTPError as e:
        print(f'Error occurred: "{e}"')
    return lang_stat


def print_statistics(data, title):
    if not data:
        print('No data to print out')
        return
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
    sj_app_key = os.getenv('SUPERJOB_APP_KEY')
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
    verbose = True
    langs_stat_hh, langs_stat_sj = {}, {}
    for prog_lang in prog_langs:
        langs_stat_hh[prog_lang] = get_statistics_hh(
            prog_lang, verbose=verbose)
        langs_stat_sj[prog_lang] = get_statistics_sj(
            sj_app_key, prog_lang, verbose=verbose)
    print_statistics(langs_stat_hh, 'HeadHunter Moscow')
    print_statistics(langs_stat_sj, 'SuperJob Moscow')
