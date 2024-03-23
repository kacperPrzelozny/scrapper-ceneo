from urllib.request import urlopen


class CeneoClient:
    url = 'https://www.ceneo.pl/'

    def request(self, productId):
        req = urlopen(CeneoClient.url + productId)
        code = req.getcode()
        if code == 200:
            return {"status": "success", "page": req.read().decode('utf-8')}
        elif code == 404:
            return {"status": "error", "message": "Product not found"}
        else:
            return {"status": "error", "message": "Something went wrong"}

