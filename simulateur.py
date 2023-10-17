import pandas as pd

betclic_data = pd.read_csv('./Data/BetclicScrap.csv')
rugby_data = pd.read_csv('./Data/RugbyDataset.csv')
zebet_data = pd.read_csv('./Data/ZebetScrap.csv')

def pourcentage_victoires(equipe):
    victoires = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] > rugby_data['away_score'])])
    victoires += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] > rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return (victoires / total_matchs) * 100

def pourcentage_defaites(equipe):
    defaites = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] < rugby_data['away_score'])])
    defaites += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] < rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return (defaites / total_matchs) * 100

def pourcentage_matchs_nuls(equipe):
    matchs_nuls = len(rugby_data[((rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)) & (rugby_data['home_score'] == rugby_data['away_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return (matchs_nuls / total_matchs) * 100

equipe1 = input("Saisissez le nom de la première équipe : ")
equipe2 = input("Saisissez le nom de la deuxième équipe : ")

pourcentage_victoires_equipe1 = pourcentage_victoires(equipe1)
pourcentage_defaites_equipe1 = pourcentage_defaites(equipe1)
pourcentage_matchs_nuls_equipe1 = pourcentage_matchs_nuls(equipe1)

pourcentage_victoires_equipe2 = pourcentage_victoires(equipe2)
pourcentage_defaites_equipe2 = pourcentage_defaites(equipe2)
pourcentage_matchs_nuls_equipe2 = pourcentage_matchs_nuls(equipe2)

cote_equipe1 = float(betclic_data.loc[betclic_data['Pays 1'] == equipe1]['Cote 1'].str.replace(',', '.').values[0])
cote_equipe2 = float(betclic_data.loc[betclic_data['Pays 1'] == equipe2]['Cote 1'].str.replace(',', '.').values[0])

proba_victoire_equipe1 = 1 / cote_equipe1
proba_victoire_equipe2 = 1 / cote_equipe2

score_equipe1 = pourcentage_victoires_equipe1 - pourcentage_defaites_equipe1 + pourcentage_matchs_nuls_equipe1
score_equipe2 = pourcentage_victoires_equipe2 - pourcentage_defaites_equipe2 + pourcentage_matchs_nuls_equipe2

score_combine_equipe1 = score_equipe1 * proba_victoire_equipe1
score_combine_equipe2 = score_equipe2 * proba_victoire_equipe2

if score_combine_equipe1 > score_combine_equipe2:
    gagnant = equipe1
elif score_combine_equipe2 > score_combine_equipe1:
    gagnant = equipe2
else:
    gagnant = "Match nul"

print(f"Statistiques pour {equipe1}:")
print(f"Pourcentage de victoires : {pourcentage_victoires_equipe1:.2f}%")
print(f"Pourcentage de défaites : {pourcentage_defaites_equipe1:.2f}%")
print(f"Pourcentage de matchs nuls : {pourcentage_matchs_nuls_equipe1:.2f}%")
print()
print(f"Statistiques pour {equipe2}:")
print(f"Pourcentage de victoires : {pourcentage_victoires_equipe2:.2f}%")
print(f"Pourcentage de défaites : {pourcentage_defaites_equipe2:.2f}%")
print(f"Pourcentage de matchs nuls : {pourcentage_matchs_nuls_equipe2:.2f}%")

print(f"Selon les statistiques et les cotes de Betclic, l'équipe gagnante est : {gagnant}")
