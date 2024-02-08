import requests
import discord
import asyncio
import os

TOKEN = os.environ.get('DISCORD_API')
CHANNEL_ID = '1203129432911519804'  # Utilisez l'ID de canal approprié
OPENSEA_API_KEY = os.environ.get('OPENSEA_API_KEY')
COLLECTION_SLUG = 'zorbs-eth'

headers = {
    "X-API-KEY": OPENSEA_API_KEY,
    "Accept": "application/json"
}

client = discord.Client(intents=discord.Intents.default())

async def get_lowest_price_listing():
    url = f"https://api.opensea.io/api/v2/listings/collection/{COLLECTION_SLUG}/all"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        listings = response.json()['listings']
        if listings:  # Vérifier si la liste des listings n'est pas vide
            lowest_price_listing = min(
                listings,
                key=lambda x: float(x['price']['current']['value']) / (10 ** x['price']['current']['decimals'])
            )
            return lowest_price_listing
        else:
            return None
    else:
        print(f"Failed to get data: {response.status_code}, response: {response.text}")
        return None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(int(CHANNEL_ID))
    if channel is None:
        print(f"Channel with ID {CHANNEL_ID} not found.")
        return

    while True:
        lowest_price_listing = await get_lowest_price_listing()
        if lowest_price_listing:
            lowest_price_value = lowest_price_listing['price']['current']['value']
            lowest_price_eth = float(lowest_price_value) / (10 ** 18)  # Convertir de wei en ether
            if lowest_price_eth > 0.025:
                token_id = lowest_price_listing['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
                contract_address = lowest_price_listing['protocol_data']['parameters']['offer'][0]['token']
                listing_url = f"https://opensea.io/assets/{contract_address}/{token_id}"
                await channel.send(f"Le prix le plus bas de la collection est actuellement : {lowest_price_eth} ETH\nLien du listing: {listing_url}")
            elif lowest_price_eth < 0.025:
                await channel.send(f"@everyone Grosse dinguerrie les Zorb sont désormais à : {lowest_price_eth} ETH\nLien du listing: {listing_url}")

        else:
            print("Aucun listing trouvé ou impossible de récupérer les listings.")

        await asyncio.sleep(600)  # Attendre 5 minutes avant de répéter la vérification

client.run(TOKEN)
