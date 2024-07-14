# # Importer les bibliothèques nécessaires
# import requests
# import pandas as pd
#
# # Initialiser le client ID et le client secret depuis Spotify Developer Dashboard
# CLIENT_ID = 'df09b4b6c3854a9ba79dd927cc3c0886'
# CLIENT_SECRET = '48eb4fe934084c918495efdf3a4307fa'
#
# # Récupérer un jeton d'accès depuis Spotify
# auth_response = requests.post(
#     'https://accounts.spotify.com/api/token',
#     data={'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
# )
# auth_data = auth_response.json()
# access_token = auth_data['access_token']
#
# # Préparer les en-têtes pour les requêtes API
# headers = {'Authorization': f'Bearer {access_token}'}
#
# # Charger votre fichier CSV existant dans un DataFrame
# # Remplacez 'path/to/your/csv/file.csv' par le chemin réel vers votre fichier
# df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
#
# # Créer une liste vide pour stocker les URLs des couvertures
# cover_urls = []
#
# # Boucler à travers chaque ligne du DataFrame pour rechercher les pistes sur Spotify
# for _, row in df.iterrows():
#     track_name = row['track_name']
#     artist_name = row['artist(s)_name']
#
#     # Construire la requête de recherche
#     query = f"track:{track_name} artist:{artist_name}"
#     search_response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
#     search_data = search_response.json()
#
#     try:
#         cover_url = search_data['tracks']['items'][0]['album']['images'][0]['url']
#     except (KeyError, IndexError):
#         cover_url = 'Not Found'
#
#     cover_urls.append(cover_url)
#
# # Ajouter la liste des URLs des couvertures comme nouvelle colonne au DataFrame
# df['cover_url'] = cover_urls
#
# # Enregistrer le DataFrame mis à jour dans un nouveau fichier CSV
# df.to_csv('updated_spotify_data.csv', index=False)
#
# print('Le DataFrame mis à jour a été enregistré dans updated_spotify_data.csv')


import requests
import pandas as pd
import time
from urllib.parse import quote

# Initialiser le client ID et le client secret depuis Spotify Developer Dashboard
CLIENT_ID = 'df09b4b6c3854a9ba79dd927cc3c0886'
CLIENT_SECRET = '48eb4fe934084c918495efdf3a4307fa'

# Récupérer un jeton d'accès depuis Spotify
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
)
auth_data = auth_response.json()
access_token = auth_data['access_token']

# Préparer les en-têtes pour les requêtes API
headers = {'Authorization': f'Bearer {access_token}'}

# Charger votre fichier CSV existant dans un DataFrame
# Remplacez 'path/to/your/csv/file.csv' par le chemin réel vers votre fichier
df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Créer une liste vide pour stocker les URLs des couvertures
cover_urls = []


# Fonction pour effectuer une requête API avec gestion des erreurs
def make_request(url, headers, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Erreur de connexion: {e}. Nouvelle tentative {i + 1}/{retries}")
            time.sleep(2)  # Attendre un peu avant de réessayer
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            break
    return None


# Boucler à travers chaque ligne du DataFrame pour rechercher les pistes sur Spotify
for _, row in df.iterrows():
    track_name = row['track_name']
    artist_name = row['artist(s)_name']

    # Construire la requête de recherche
    query = f"track:{quote(track_name)} artist:{quote(artist_name)}"
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    search_data = make_request(search_url, headers)

    if search_data:
        try:
            cover_url = search_data['tracks']['items'][0]['album']['images'][0]['url']
        except (KeyError, IndexError):
            cover_url = 'Not Found'
    else:
        cover_url = 'Not Found'

    cover_urls.append(cover_url)

# Ajouter la liste des URLs des couvertures comme nouvelle colonne au DataFrame
df['cover_url'] = cover_urls

# Enregistrer le DataFrame mis à jour dans un nouveau fichier CSV
df.to_csv('updated_spotify_data.csv', index=False)

print('Le DataFrame mis à jour a été enregistré dans updated_spotify_data.csv')

