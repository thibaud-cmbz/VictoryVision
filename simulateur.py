import pandas as pd

# Charger les données à partir des fichiers CSV
betclic_data = pd.read_csv('./Data/BetclicScrap.csv')
rugby_data = pd.read_csv('./Data/RugbyDataset.csv')
zebet_data = pd.read_csv('./Data/ZebetScrap.csv')

# Fonction pour calculer le pourcentage de victoires d'une équipe
def pourcentage_victoires(equipe):
    victoires = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] > rugby_data['away_score'])])
    victoires += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] > rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0  # Aucun match joué
    return (victoires / total_matchs) * 100

# Fonction pour calculer le pourcentage de défaites d'une équipe
def pourcentage_defaites(equipe):
    defaites = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] < rugby_data['away_score'])])
    defaites += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] < rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0  # Aucun match joué
    return (defaites / total_matchs) * 100

# Fonction pour calculer le pourcentage de matchs nuls d'une équipe
def pourcentage_matchs_nuls(equipe):
    matchs_nuls = len(rugby_data[((rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)) & (rugby_data['home_score'] == rugby_data['away_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0  # Aucun match joué
    return (matchs_nuls / total_matchs) * 100

# Demander à l'utilisateur de choisir deux équipes
equipe1 = input("Saisissez le nom de la première équipe : ")
equipe2 = input("Saisissez le nom de la deuxième équipe : ")

# Calculer les statistiques pour chaque équipe
pourcentage_victoires_equipe1 = pourcentage_victoires(equipe1)
pourcentage_defaites_equipe1 = pourcentage_defaites(equipe1)
pourcentage_matchs_nuls_equipe1 = pourcentage_matchs_nuls(equipe1)

pourcentage_victoires_equipe2 = pourcentage_victoires(equipe2)
pourcentage_defaites_equipe2 = pourcentage_defaites(equipe2)
pourcentage_matchs_nuls_equipe2 = pourcentage_matchs_nuls(equipe2)

# Simulez le match en fonction des cotes et des statistiques
cote_equipe1 = float(betclic_data.loc[betclic_data['Pays 1'] == equipe1]['Cote 1'].str.replace(',', '.').values[0])
cote_equipe2 = float(betclic_data.loc[betclic_data['Pays 1'] == equipe2]['Cote 1'].str.replace(',', '.').values[0])

# Calculer les probabilités basées sur les cotes
proba_victoire_equipe1 = 1 / cote_equipe1
proba_victoire_equipe2 = 1 / cote_equipe2

# Calculer les scores en fonction des statistiques
score_equipe1 = pourcentage_victoires_equipe1 - pourcentage_defaites_equipe1 + pourcentage_matchs_nuls_equipe1
score_equipe2 = pourcentage_victoires_equipe2 - pourcentage_defaites_equipe2 + pourcentage_matchs_nuls_equipe2

# Combinaison des probabilités et des scores
score_combine_equipe1 = score_equipe1 * proba_victoire_equipe1
score_combine_equipe2 = score_equipe2 * proba_victoire_equipe2

# Comparer les scores pour déterminer le gagnant
if score_combine_equipe1 > score_combine_equipe2:
    gagnant = equipe1
elif score_combine_equipe2 > score_combine_equipe1:
    gagnant = equipe2
else:
    gagnant = "Match nul"

# Afficher les statistiques pour chaque équipe
print(f"Statistiques pour {equipe1}:")
print(f"Pourcentage de victoires : {pourcentage_victoires_equipe1:.2f}%")
print(f"Pourcentage de défaites : {pourcentage_defaites_equipe1:.2f}%")
print(f"Pourcentage de matchs nuls : {pourcentage_matchs_nuls_equipe1:.2f}%")
print()
print(f"Statistiques pour {equipe2}:")
print(f"Pourcentage de victoires : {pourcentage_victoires_equipe2:.2f}%")
print(f"Pourcentage de défaites : {pourcentage_defaites_equipe2:.2f}%")
print(f"Pourcentage de matchs nuls : {pourcentage_matchs_nuls_equipe2:.2f}%")

# Affichez le résultat de la simulation
print(f"Selon les statistiques et les cotes de Betclic, l'équipe gagnante est : {gagnant}")
