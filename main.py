import requests
import json
import pandas as pd


json_objects = []


def get_hours(i, j):
    for page in range(0, 20):
        js_obj = json.loads(get_content(i, j, page))
        json_objects.extend(js_obj["items"])
        if (js_obj['pages'] - page) <= 1:
            break


def get_content(i, j, page=0):
    params = {
        'specialization': 1,
        'date_from': f'2022-12-16T{i}:00:01+0300',
        'date_to': f'2022-12-16T{j}:59:59+0300',
        'page': page,
        'per_page': 100
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data


def extract_from_dict(first_value, second_value):
    result = []
    for i in range(0, len(first_value)):
        if first_value[i] is None:
            result.append(first_value[i])
        else:
            result.append(first_value[i][second_value])
    return result


get_hours('00', '03')
get_hours('04', '06')
get_hours('07', '09')
get_hours('10', '12')
get_hours('13', '15')
get_hours('16', '18')
get_hours('19', '21')
get_hours('22', '23')


def get_params(name, salary_from, salary_to, salary_currency, area_name, published_at):
    for i in range(0, len(json_objects)) :
        name.append(json_objects[i]['name'])
        salary_from.append(json_objects[i]['salary'])
        salary_to.append(json_objects[i]['salary'])
        salary_currency.append(json_objects[i]['salary'])
        area_name.append(json_objects[i]['area'])
        published_at.append(json_objects[i]['published_at'])
    dict_params = {
        'name': name,
        'salary_from': extract_from_dict(salary_from, 'from'),
        'salary_to': extract_from_dict(salary_to, 'to'),
        'salary_currency': extract_from_dict(salary_currency, 'currency'),
        'area_name': extract_from_dict(area_name, 'name'),
        'published_at': published_at
    }
    return dict_params


if __name__ == '__main__':
    name = []
    salary_from = []
    salary_to = []
    salary_currency = []
    area_name = []
    published_at = []
    params = get_params(name, salary_from, salary_to, salary_currency, area_name, published_at)
    dict_df = pd.DataFrame(params)
    dict_df.to_csv('data.csv', index=False)
