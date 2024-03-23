from app.Model.Product import Product
from app.Services.CeneoClient import CeneoClient
from bs4 import BeautifulSoup


class CeneoScrapperService:
    def __init__(self, productId):
        self.productId = productId
        self.client = CeneoClient()

    def getProduct(self):
        response = self.client.request(self.productId)

        if response["status"] != "success":
            return {"status": "error"}

        soup = BeautifulSoup(response["page"], 'html.parser')
        name = self.getName(soup)
        opinions_count = self.getOpinionsCount(soup)
        average_mark = self.getAverageMark(soup)

        product = Product(self.productId, name, opinions_count, average_mark)
        product.save()

        return product

    def getName(self, soup):
        return soup.find("h1", class_="product-top__product-info__name").text

    def getOpinionsCount(self, soup):
        return soup.find("div", class_="score-extend__review").text.replace(" opinii", "")

    def getAverageMark(self, soup):
        return float(soup.find("div", class_="review-header__score").find("font").text.replace(',', '.'))