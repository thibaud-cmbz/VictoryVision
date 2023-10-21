from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Charger les datasets
rugby_data = pd.read_csv('./Data/RugbyDataset.csv')
team_rugby = pd.read_csv('./Data/TeamRugby.csv')
betclic_scrap_fix = pd.read_csv('./Data/BetClicScrapFix.csv')

# Fonction pour calculer le poids en fonction de l'année
current_year = datetime.now().year

def calculate_year_weight(row_date):
    confrontation_year = pd.to_datetime(row_date).year
    if current_year - confrontation_year <= 20:
        return 1.0  # Événements récents valent 100%
    elif current_year - confrontation_year <= 40:
        return 0.6  # Événements de 20 à 40 ans valent 60%
    else:
        return 0.3  # Événements de plus de 40 ans valent 30%

team_rugby['YearWeight'] = team_rugby['date'].apply(calculate_year_weight)

# Fonction pour calculer la moyenne des essais marqués en prenant en compte le poids de l'année
def average_tries_scored(equipe, dataframe):
    team_data = dataframe[dataframe['Team'] == equipe]
    weighted_average = (team_data['TF'] * team_data['YearWeight']).sum() / team_data['YearWeight'].sum()
    return weighted_average

# Fonction pour prédire le nombre d'essais en fonction de la probabilité et de la moyenne des essais
def predict_tries(prob, avg_tries):
    if prob >= 0.5:
        return round(avg_tries * (1 + (prob - 0.5) * 2))
    else:
        return round(avg_tries * (1 - (0.5 - prob) * 2))

# Fonction pour calculer la probabilité d'une équipe de gagner
def proba_team(equipe, opponent, dataframe):
    win_rows = len(dataframe[(dataframe['Team'] == equipe) & (dataframe['Opponent'] == opponent) & (dataframe['Result'] == "W")])
    total_matches = len(dataframe[(dataframe['Team'] == equipe) & (dataframe['Opponent'] == opponent)])
    return win_rows / total_matches if total_matches != 0 else 0.0

# Fonction pour calculer la probabilité d'une équipe d'opposition de gagner
def proba_opponent(equipe, opponent, dataframe):
    loss_rows = len(dataframe[(dataframe['Team'] == equipe) & (dataframe['Opponent'] == opponent) & (dataframe['Result'] == "L")])
    total_matches = len(dataframe[(dataframe['Team'] == equipe) & (dataframe['Opponent'] == opponent)])
    return loss_rows / total_matches if total_matches != 0 else 0.0

# Fonction pour calculer les probabilités combinées en utilisant les deux datasets
def calculate_percentage_chances(equipe1, equipe2):
    exist_in_betclic = (equipe1 in betclic_scrap_fix['Team'].values) and (equipe2 in betclic_scrap_fix['Opponent'].values)
    exist_in_team_rugby = (equipe1 in team_rugby['Team'].values) and (equipe2 in team_rugby['Opponent'].values)
    
    if exist_in_betclic and exist_in_team_rugby:
        prob_team1_betclic = proba_team(equipe1, equipe2, betclic_scrap_fix)
        prob_team2_betclic = proba_opponent(equipe1, equipe2, betclic_scrap_fix)

        prob_team1_rugby = proba_team(equipe1, equipe2, team_rugby)
        prob_team2_rugby = proba_opponent(equipe1, equipe2, team_rugby)

        combined_prob_team1 = 0.65 * prob_team1_betclic + 0.35 * prob_team1_rugby
        combined_prob_team2 = 0.65 * prob_team2_betclic + 0.35 * prob_team2_rugby
    elif exist_in_team_rugby:
        combined_prob_team1 = proba_team(equipe1, equipe2, team_rugby)
        combined_prob_team2 = proba_opponent(equipe1, equipe2, team_rugby)
    else:
        return {"team1": 0.5, "team2": 0.5}

    total_prob = combined_prob_team1 + combined_prob_team2
    return {"team1": combined_prob_team1 / total_prob, "team2": combined_prob_team2 / total_prob}

# Fonction pour calculer la cote théorique
def calculate_theoretical_odds(equipe, dataframe):
    total_wins = len(dataframe[(dataframe['Team'] == equipe) & (dataframe['Result'] == "W")])
    theoretical_odds = 1 / (total_wins / len(dataframe) / 100)
    return theoretical_odds / 100

# Liste des équipes disponibles
teams = team_rugby['Team'].unique().tolist()

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html', teams=teams)

# Route pour la prédiction
@app.route('/results', methods=['POST'])
def predict():
    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')

    # Calcul des probabilités et essais prédits
    results = calculate_percentage_chances(equipe1, equipe2)
    avg_tries_team1 = average_tries_scored(equipe1, team_rugby)
    avg_tries_team2 = average_tries_scored(equipe2, team_rugby)
    predicted_tries_team1 = predict_tries(results['team1'], avg_tries_team1)
    predicted_tries_team2 = predict_tries(results['team2'], avg_tries_team2)

    # Calcul de la cote théorique
    cote_equipe1 = calculate_theoretical_odds(equipe1, team_rugby)
    cote_equipe2 = calculate_theoretical_odds(equipe2, team_rugby)

    # Calcul des pourcentages de victoires, défaites et matchs nuls
    percentage_victoires_equipe1 = results['team1'] * 100
    percentage_victoires_equipe2 = results['team2'] * 100
    percentage_defaites_equipe1 = (1 - results['team1']) * 100
    percentage_defaites_equipe2 = (1 - results['team2']) * 100
    percentage_matchs_nuls_equipe1 = 100 - percentage_victoires_equipe1 - percentage_defaites_equipe1
    percentage_matchs_nuls_equipe2 = 100 - percentage_victoires_equipe2 - percentage_defaites_equipe2

    return render_template('results.html', equipe1=equipe1, equipe2=equipe2, 
                           prob_team1=results['team1'], prob_team2=results['team2'],
                           avg_tries_team1=avg_tries_team1, avg_tries_team2=avg_tries_team2,
                           predicted_tries_team1=predicted_tries_team1, predicted_tries_team2=predicted_tries_team2,
                           cote_equipe1=cote_equipe1, cote_equipe2=cote_equipe2,
                           percentage_victoires_equipe1=percentage_victoires_equipe1,
                           percentage_victoires_equipe2=percentage_victoires_equipe2,
                           percentage_defaites_equipe1=percentage_defaites_equipe1,
                           percentage_defaites_equipe2=percentage_defaites_equipe2,
                           percentage_matchs_nuls_equipe1=percentage_matchs_nuls_equipe1,
                           percentage_matchs_nuls_equipe2=percentage_matchs_nuls_equipe2)

if __name__ == '__main__':
    app.run(debug=True)
