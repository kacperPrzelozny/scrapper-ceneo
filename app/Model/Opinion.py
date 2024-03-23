from app.Model.Model import Model
from app.Model.Product import Product


class Opinion(Model):

    def __init__(self, id, product_id, author, recommendation, stars, is_opinion_confirmed_by_purchase, date_of_opinion, date_of_purchase, likes, dislikes, content):
        self.id = id
        self.product_id = product_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.is_opinion_confirmed_by_purchase = is_opinion_confirmed_by_purchase
        self.date_of_opinion = date_of_opinion
        self.date_of_purchase = date_of_purchase
        self.likes = likes
        self.dislikes = dislikes
        self.content = content

        self.product = Product.findById(self.product_id)