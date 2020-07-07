# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
import string


def get_full_data():
    """
    generate csv of all the data about the bac available datas
    """

    out = []

    # bac général
    bac = 12  # numéro du bac général

    for dep in ['067', '068']:  # département

        for filiere in ['ES', 'S', 'L']:  # filière générale

            out += get_data(filiere, key=bac, dep=dep)

    # bac technologique
    bac = 14  # numéro du bac technologique

    for filiere in ['STHR', 'STI2D', 'ST2S', 'STD2A', 'STMG', 'STL']:  # filière technologique

        out += get_data(filiere, key=bac)

    save_csv(sorted(out), 'Résultat du bac général et technologique en Alsace')

    return out


def get_data(filiere, key=12, dep='', save=True, text=True):
    """
    filiere : the name of the filiere, like ES, S, L, or STI2D, STMG
    key : the number of the bac, 12 if general and 14 if techno
    dep : the number of the departement, ex : 067 for bas rhin, WARNING ONLY USE IF KEY = 12
    returns a list of lists containing the name in pos 0 and the result in pos 1,
        ex : [[SURNAME1 Name1, RESULT1], [SURNAME2 Name2, RESULT2]]
    """
    if text:
        print(f'- Obtention des données de la filière {filiere}')

    output_rows = []

    for letter in string.ascii_uppercase:  # alphabet

        if dep != '' and not dep.endswith('_'):
            dep += '_'

        url = f'http://e-resultats.ac-strasbourg.fr/resultats_{key}_{dep}{filiere}_{letter}.html'

        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        tables = soup.find_all('table', attrs={'class': 'tableauResultat'})  # get only the tables of each pages

        for table in tables:

            table_data = table.tbody.find_all("tr")

            for table_row in table_data:
                columns = table_row.findAll('td')
                output_row = []
                for column in columns:
                    output_row.append(column.text)
                output_rows.append(output_row)

    if save:
        save_csv(output_rows, f'tables/{dep}{filiere}.csv')

    if text:
        print(f'+ Données de la filière {filiere} obtenues')

    return output_rows


def save_csv(data, name):
    """
    save data into a csv file named name
    """
    if not name.endswith('.csv'):
        name += '.csv'

    with open(name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)
