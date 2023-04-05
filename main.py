import requests, uuid, time, json

with open('config.json') as config:
    config = json.load(config)

assetId = input('enter assetid: ')
amount = int(input('purchase howmany times: '))

class Bot:
    def __init__(self):
        self.session = requests.Session()
        self.session.cookies['.ROBLOSECURITY'] = config['cookie']
        self.user_id = self.session.get('https://www.roblox.com/my/settings/json').json()['UserId']

    def csrf_token(self):
        return self.session.post('https://auth.roblox.com/v2/login').headers['x-csrf-token']

    def item_info(self):
        self.collectible_id = self.session.get(f'https://catalog.roblox.com/v1/catalog/items/{assetId}/details?itemType=Asset').json()['collectibleItemId']
        item_data = self.session.post(
            'https://apis.roblox.com/marketplace-items/v1/items/details',
            json = {"itemIds": [self.collectible_id]}, headers = {'x-csrf-token': self.csrf_token()}
        ).json()[0]
        self.product_id = item_data['collectibleProductId']
        self.asset_price = item_data['price']
        self.seller_id = item_data['creatorId']

    def purchase_item(self):
        for i in range(amount):
            response = self.session.post(
                f'https://apis.roblox.com/marketplace-sales/v1/item/{self.collectible_id}/purchase-item',
                json = {
                    "collectibleItemId": self.collectible_id,
                    "expectedCurrency": 1,
                    "expectedPrice": self.asset_price,
                    "expectedPurchaserId": str(self.user_id),
                    "expectedPurchaserType": "User",
                    "expectedSellerId": 1,
                    "expectedSellerType": "User",
                    "idempotencyKey": str(uuid.uuid4()),
                    "collectibleProductId": self.product_id
                },
                headers = {
                    'X-CSRF-TOKEN': self.csrf_token()
                }
            )
            print(response.json())
        
a = Bot()
a.item_info()
a.purchase_item()
