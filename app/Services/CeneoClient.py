from urllib.error import HTTPError
from urllib.request import urlopen


class CeneoClient:
    url = 'https://www.ceneo.pl'

    def request(self, productId):
        try:
            req = urlopen(CeneoClient.url + productId)
        except HTTPError as e:
            return {"status": "error", "message": "Something went wrong"}

        code = req.getcode()
        if code == 200:
            return {"status": "success", "page": req.read().decode('utf-8')}

