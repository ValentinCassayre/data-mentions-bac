# -*- coding: utf-8 -*-

from get_data import get_full_data, get_data, save_csv
from search_data import search_mention, search_file, count

# example of what you can do
# exemple de ce que tu peux faire

# get the full data
# récupérer toutes les données
full_data = get_full_data()

# get a specific data
# récupérer des données spécifiques
data = get_data(filiere='S', dep='067', text=False)
data += get_data(filiere='S', dep='068', text=False)

# save the data into a csv
# sauvegarder les données dans un fichier csv (tableur)
save_csv(data, name='Resultat bac alsace filière scientifique')

# count the number of mentions
# compte le nombre de mentions obtenues dans la séries de données
count(data, write_json=True)

# search in the data if someone has the mention (name and mention_macron are both strings)
# cherche dans les données la mention d'une personne spécifique
# (name et mention_macron sont tous les deux des chaines de caractères)
mention_macron = search_mention(data, name='MACRON Emmanuel')

# search in the data a full list of names
# rechercher dans les données les mentions d'une liste entières de noms (à compléter dans input.txt)
# résultat dans output.csv avec stats dans stats.json
search_file(data, 'input.txt')
