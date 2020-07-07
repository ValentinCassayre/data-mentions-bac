# -*- coding: utf-8 -*-

import unidecode
import json


def search_mention(data, name):
    """
    return the result of someone named name in the format SURNAME Name
    data is the data in which it needs to search
    data is in the form [[SURNAME1 Name1, RESULT1], [SURNAME2 Name2, RESULT2]]
    """

    name = unidecode.unidecode(name)

    names = list(map(lambda x: unidecode.unidecode(x[0]), data))
    mentions = list(map(lambda x: x[1], data))

    try:
        return mentions[names.index(name)]
    except ValueError:
        return 'PAS PUBLIQUE'


def search_file(data, file_name='input.txt', stats=False):
    """
    search the mention of all the people on the file named file_name
    data is the data in which it needs to search
    data is in the form [[SURNAME1 Name1, RESULT1], [SURNAME2 Name2, RESULT2]]
    if stats is True it will calculate the stats and save it in stats.json
    """

    out = []

    if not file_name.endswith('.txt'):
        file_name = f'{file_name}.txt'

    with open(file_name, 'r', encoding='utf-8') as reader:
        with open('output.csv', 'w', encoding='utf-8') as writer:

            names = reader.read().split('\n')

            for name in names:

                name = name.replace('\t', ' ')
                anotation = search_mention(data, name)

                out.append((name, anotation))
                writer.write(f'{name};{anotation}\n')

    if stats:
        count(out)

    return out


def count(data, write_json=True):
    """
    allows to create stats about a list of results from the form data
    data is in the form [[SURNAME1 Name1, RESULT1], [SURNAME2 Name2, RESULT2]]
    """

    mentions = ['ADMIS MENTION TRES BIEN', 'ADMIS MENTION BIEN', 'ADMIS MENTION ASSEZ BIEN', 'ADMIS',
                'INSCRIT EPREUVES REPORTEES', 'PASSE SECOND GROUPE']

    options = ['section europeenne']

    stats = {'mentions': {}, 'options': {}}

    for person_info in data:
        for mention in mentions:
            if person_info[1].startswith(mention):
                try:
                    stats['mentions'][mention] += 1
                except KeyError:
                    stats['mentions'][mention] = 1
                break

        for option in options:
            if person_info[1].endswith(option):
                try:
                    stats['options'][option] += 1
                except KeyError:
                    stats['options'][option] = 1
                break

    stats['total'] = len(data)

    if write_json:
        with open('stats.json', 'w', encoding='utf-8') as file:
            json.dump(stats, file, ensure_ascii=False, indent=4)

    return stats
