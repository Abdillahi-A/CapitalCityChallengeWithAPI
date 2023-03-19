# This script is uses the restcountries API to build the dataset for this game.
# It is not required to run this script, as the output has already been saved to data.json.
# The reason we are not using the API directly in the game, is because API's can change, and having the dataset hardcoded
# ensures that the game will always work.
import requests
import json

# use the restcountries api to build dataset
response = requests.get('https://restcountries.com/v3.1/all?fields=region,name,flags,unMember,capital')
response_json = json.loads(response.text)


data = {}
for i in response_json:
    continent = i['region']
    country = i['name']['common']
    unMember = i['unMember']
    flag = i['flags']['png']
    capital = i['capital']

    # only include UN member states and ignore antarctic
    if continent == 'Antarctic' or not unMember :
        continue
    else:
        if continent not in data.keys():
            # add continents to dictionary
            data[continent] = []
        # add countries and flags to continents
        data[continent].append({'Country':country, 'Capital':capital[0],'Flag':flag})

# save to 
with open("data.json", "w") as f:
    json.dump(data,f) 

