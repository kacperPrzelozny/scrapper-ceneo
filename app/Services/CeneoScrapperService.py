from app.Model.Feature import Feature
from app.Model.Opinion import Opinion
from app.Model.Product import Product
from app.Services.CeneoClient import CeneoClient
from bs4 import BeautifulSoup


class CeneoScrapperService:
    def __init__(self, productId):
        self.productId = productId
        self.client = CeneoClient()

    def getProduct(self):
        response = self.client.request(f"/{self.productId}")

        if response["status"] != "success":
            return {"status": "error", "message": response["message"]}

        soup = BeautifulSoup(response["page"], 'html.parser')
        name = self.getName(soup)
        opinions_count = self.getOpinionsCount(soup)
        average_mark = self.getAverageMark(soup)

        product = Product(self.productId, name, opinions_count, average_mark)
        product.setOpinions(self.getOpinions(soup, product))
        product.save()

    def getName(self, soup):
        return soup.find("h1", class_="product-top__product-info__name").text

    def getOpinionsCount(self, soup):
        return soup.find("div", class_="score-extend__review").text.replace(" opinii", "").replace(" opinia", "").replace(" opinie", "")

    def getAverageMark(self, soup):
        return float(soup.find("div", class_="review-header__score").find("font").text.replace(',', '.'))

    def getOpinions(self, soup, product):
        opinionsDiv = soup.find("div", class_="js_product-reviews-container")
        userPosts = opinionsDiv.find_all('div', class_="user-post__card")
        opinions = []
        for userPost in userPosts:
            opinionData = self.getOpinionData(userPost, product)

            opinion = Opinion(*opinionData)
            opinion.setProductId(product)
            opinion.setFeatures(self.getFeaturesData(userPost))
            for feature in opinion.features:
                feature.setProduct(product)

            opinions.append(opinion)

        opinions = self.processNextPage(opinions, soup, product)
        return opinions

    def processNextPage(self, opinions, soup, product):
        pagination = soup.find("div", class_="pagination")
        if pagination is None:
            return opinions

        nextButton = pagination.find('a', class_="pagination__item pagination__next")
        if nextButton is None:
            return opinions

        response = self.client.request(nextButton.get('href'))
        soup = BeautifulSoup(response["page"], 'html.parser')

        return opinions + self.getOpinions(soup, product)

    def getOpinionData(self, userPost, product):
        opinionId = userPost.get('data-entry-id')
        author = userPost.find('span', class_="user-post__author-name").text.strip()
        recommendationsSpan = userPost.find('span', class_="user-post__author-recomendation")
        recommendations = None if recommendationsSpan is None else recommendationsSpan.find('em').text
        stars = float(userPost.find('span', class_="user-post__score-count").text.split('/')[0].replace(',', '.'))
        is_opinion_confirmed_by_purchase = True if userPost.find('div', class_="review-pz") is not None else False
        dates = userPost.find_all('time')
        try:
            date_of_opinion = dates[0].get('datetime')
        except IndexError:
            date_of_opinion = None
        try:
            date_of_purchase = dates[1].get('datetime')
        except IndexError:
            date_of_purchase = None
        likes = userPost.find('button', class_="vote-yes").get('data-total-vote')
        dislikes = userPost.find('button', class_="vote-no").get('data-total-vote')
        content = userPost.find('div', class_="user-post__text").text

        return [opinionId, author, recommendations, stars, is_opinion_confirmed_by_purchase, date_of_opinion,
                date_of_purchase,
                likes, dislikes, content]

    def getFeaturesData(self, userPost):
        features = []

        featuresColumns = userPost.find_all('div', class_="review-feature__col")
        for column in featuresColumns:
            if column.find('div', class_="review-feature__title--positives") is not None:
                for featureDiv in column.find_all('div', class_="review-feature__item"):
                    feature = Feature(featureDiv.text, True)
                    features.append(feature)
            elif column.find('div', class_="review-feature__title--negatives") is not None:
                for featureDiv in column.find_all('div', class_="review-feature__item"):
                    feature = Feature(featureDiv.text, False)
                    features.append(feature)

        return features
