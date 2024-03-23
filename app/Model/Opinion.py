from app.Model.Model import Model
from app.Model.Product import Product


class Opinion(Model):

    def __init__(self, id, author, recommendation, stars, is_opinion_confirmed_by_purchase, date_of_opinion,
                 date_of_purchase, likes, dislikes, content):
        self.product = None
        self.product_id = None
        self.id = id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.is_opinion_confirmed_by_purchase = is_opinion_confirmed_by_purchase
        self.date_of_opinion = date_of_opinion
        self.date_of_purchase = date_of_purchase
        self.likes = likes
        self.dislikes = dislikes
        self.content = content

    def setProductId(self, product):
        self.product_id = product.id
        self.product = product

    def save(self):
        sql = "INSERT INTO opinions (id, product_id, author, recommendation, stars, is_opinion_confirmed_by_purchase, date_of_opinion, date_of_purchase, likes, dislikes, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        Opinion.executeQuery(sql, self.flattenObject())

    def flattenObject(self):
        return [
            self.id,
            self.product_id,
            self.author,
            self.recommendation,
            self.stars,
            self.is_opinion_confirmed_by_purchase,
            self.date_of_opinion,
            self.date_of_purchase,
            self.likes,
            self.dislikes,
            self.content
        ]
