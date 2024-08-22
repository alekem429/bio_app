import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
API_URL = config.get('api', 'url')


def get_death_types():
    response = requests.get(f'{API_URL}/get_list_of_death_types')
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_death_types_by_id(id):
    params = {"id_death_type": id} if id else {}
    response = requests.get(f'{API_URL}/get_death_for_death_type_id', params)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_list_of_factors():
    response = requests.get(f'{API_URL}/get_list_of_factors')
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_list_of_genes():
    response = requests.get(f'{API_URL}/get_list_of_genes')
    if response.status_code == 200:
        return response.json()
    else:
        return []


def add_death_type(death_name):
    data = {"name": death_name}
    response = requests.post(f'{API_URL}/add_death_type', json=data)
    return response.status_code


def add_gene(gene_name):
    data = {"name": gene_name}
    response = requests.post(f'{API_URL}/add_gene', json=data)
    return response.status_code


def add_factor(factor_name):
    data = {"name": factor_name}
    response = requests.post(f'{API_URL}/add_factor', json=data)
    return response.status_code


def delete_death_type(type_list):
    data = {"name": type_list}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{API_URL}/add_factor', json=data, headers=headers)
    return response.status_code


def delete_factors(factor_list):
    for factors in factor_list:
        data = {"name": factors}
        response = requests.post(f'{API_URL}/add_factor', json=data)


def delete_gene(gene_list):
    for gene in gene_list:
        data = {"name": gene}
        response = requests.post(f'{API_URL}/add_factor', json=data)


def delete_death(idx):
    data = {"id_death": idx}
    print(data)
    return requests.get(f'{API_URL}/remove_death', params=data).status_code
