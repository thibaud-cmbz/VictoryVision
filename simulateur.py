import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

betclic_data = pd.read_csv('./Data/BetclicScrap.csv')
rugby_data = pd.read_csv('./Data/RugbyDataset.csv')
zebet_data = pd.read_csv('./Data/ZebetScrap.csv')

equipe1 = input("Saisissez le nom de la première équipe : ")
equipe2 = input("Saisissez le nom de la deuxième équipe : ")

cote_equipe1 = betclic_data.loc[betclic_data['Pays 1'] == equipe1]['Cote 1'].values[0]
cote_equipe2 = betclic_data.loc[betclic_data['Pays 1'] == equipe2]['Cote 1'].values[0]

scores_equipe1 = rugby_data[(rugby_data['home_team'] == equipe1) & (rugby_data['away_team'] == equipe2)]
scores_equipe2 = rugby_data[(rugby_data['home_team'] == equipe2) & (rugby_data['away_team'] == equipe1)]

proba_victoire_equipe1 = 1 / float(cote_equipe1.replace(',', '.'))
proba_victoire_equipe2 = 1 / float(cote_equipe2.replace(',', '.'))

if proba_victoire_equipe1 > proba_victoire_equipe2:
    gagnant = equipe1
elif proba_victoire_equipe1 < proba_victoire_equipe2:
    gagnant = equipe2
else:
    gagnant = "Match nul"

# Afficher les résultats
print(f"Selon les données disponibles, l'équipe gagnante est : {gagnant}")
