

import requests
import json
from google.cloud import storage

def extractPokemon():
    url = "https://pokeapi.co/api/v2/pokemon/"
    pokemon_list = {"pokemon_list": list()}

    counter = 1

    while url != None:
        payload = {}
        headers = {}


        response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
        url = response["next"]

        for item in response["results"]:
            url_pokemon = "https://pokeapi.co/api/v2/pokemon/" + item["name"]
            response_pokemon = json.loads(requests.request("GET", url_pokemon, headers=headers, data=payload).text)
            info = {
                "name": item["name"],
                "id": response_pokemon["id"],
                "height": response_pokemon["height"],
                "weight": response_pokemon["weight"],
                "is_default": response_pokemon["is_default"],
            }

            pokemon_list.append(info)
            pokemon_list["pokemon_list"].append(info)
            print(response_pokemon["id"])

    bucket_name = "airflow-curso"
    bucket = storage.client().get_bucket(bucket_name)
    blob = bucket.blob("pokemonFile.json")

    with blob.open("w") as f:
        blob.upload_from_string(data=json.dumps(pokemon_list), content_type="application/json")
