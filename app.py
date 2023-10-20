from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

rugby_data = pd.read_csv('./Data/RugbyDataset.csv')

def pourcentage_victoires(equipe):
    victoires = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] > rugby_data['away_score'])])
    victoires += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] > rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return round((victoires / total_matchs) * 100, 1)

def pourcentage_defaites(equipe):
    defaites = len(rugby_data[(rugby_data['home_team'] == equipe) & (rugby_data['home_score'] < rugby_data['away_score'])])
    defaites += len(rugby_data[(rugby_data['away_team'] == equipe) & (rugby_data['away_score'] < rugby_data['home_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return round((defaites / total_matchs) * 100, 1)

def pourcentage_matchs_nuls(equipe):
    matchs_nuls = len(rugby_data[((rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)) & (rugby_data['home_score'] == rugby_data['away_score'])])
    total_matchs = len(rugby_data[(rugby_data['home_team'] == equipe) | (rugby_data['away_team'] == equipe)])
    
    if total_matchs == 0:
        return 0.0
    return round((matchs_nuls / total_matchs) * 100, 1)

def calculer_cote_theorique(pourcentage_victoires, pourcentage_defaites, pourcentage_matchs_nuls):
    cote_theorique = 1 / (pourcentage_victoires / 100)
    return round(cote_theorique, 1)

def simulate_results(equipe1, equipe2):
    pourcentage_victoires_equipe1 = pourcentage_victoires(equipe1)
    pourcentage_defaites_equipe1 = pourcentage_defaites(equipe1)
    pourcentage_matchs_nuls_equipe1 = pourcentage_matchs_nuls(equipe1)

    pourcentage_victoires_equipe2 = pourcentage_victoires(equipe2)
    pourcentage_defaites_equipe2 = pourcentage_defaites(equipe2)
    pourcentage_matchs_nuls_equipe2 = pourcentage_matchs_nuls(equipe2)

    cote_equipe1 = calculer_cote_theorique(pourcentage_victoires_equipe1, pourcentage_defaites_equipe1, pourcentage_matchs_nuls_equipe1)
    cote_equipe2 = calculer_cote_theorique(pourcentage_victoires_equipe2, pourcentage_defaites_equipe2, pourcentage_matchs_nuls_equipe2)

    proba_victoire_equipe1 = 1 / cote_equipe1
    proba_victoire_equipe2 = 1 / cote_equipe2

    score_equipe1 = pourcentage_victoires_equipe1 - pourcentage_defaites_equipe1 + pourcentage_matchs_nuls_equipe1
    score_equipe2 = pourcentage_victoires_equipe2 - pourcentage_defaites_equipe2 + pourcentage_matchs_nuls_equipe2

    score_theorique_equipe1 = round(cote_equipe2 / (cote_equipe1 + cote_equipe2) * 100, 1)
    score_theorique_equipe2 = round(cote_equipe1 / (cote_equipe1 + cote_equipe2) * 100, 1)

    if score_equipe1 > score_equipe2:
        gagnant = equipe1
    elif score_equipe2 > score_equipe1:
        gagnant = equipe2
    else:
        gagnant = "Match nul"

    return gagnant, cote_equipe1, cote_equipe2, score_theorique_equipe1, score_theorique_equipe2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    gagnant, cote_equipe1, cote_equipe2, score_theorique_equipe1, score_theorique_equipe2 = simulate_results(equipe1, equipe2)

    pourcentage_victoires_equipe1 = pourcentage_victoires(equipe1)
    pourcentage_defaites_equipe1 = pourcentage_defaites(equipe1)
    pourcentage_matchs_nuls_equipe1 = pourcentage_matchs_nuls(equipe1)

    pourcentage_victoires_equipe2 = pourcentage_victoires(equipe2)
    pourcentage_defaites_equipe2 = pourcentage_defaites(equipe2)
    pourcentage_matchs_nuls_equipe2 = pourcentage_matchs_nuls(equipe2)

    return render_template('results.html', equipe1=equipe1, equipe2=equipe2, gagnant=gagnant,
                           pourcentage_victoires_equipe1=pourcentage_victoires_equipe1,
                           pourcentage_defaites_equipe1=pourcentage_defaites_equipe1,
                           pourcentage_matchs_nuls_equipe1=pourcentage_matchs_nuls_equipe1,
                           pourcentage_victoires_equipe2=pourcentage_victoires_equipe2,
                           pourcentage_defaites_equipe2=pourcentage_defaites_equipe2,
                           pourcentage_matchs_nuls_equipe2=pourcentage_matchs_nuls_equipe2,
                           cote_equipe1=cote_equipe1,
                           cote_equipe2=cote_equipe2,
                           score_theorique_equipe1=score_theorique_equipe1,
                           score_theorique_equipe2=score_theorique_equipe2)

if __name__ == '__main__':
    app.run(debug=True)
