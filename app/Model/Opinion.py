import math

from app.Model.Model import Model


class Opinion(Model):

    fields = [
        "id", "product_id", "author", "recommendation", "stars", "is_opinion_confirmed_by_purchase", "date_of_opinion",
        "date_of_purchase", "likes", "dislikes", "content"
    ]

    displayFields = [
        "id", "author", "recommendation", "stars", "is_opinion_confirmed_by_purchase", "date_of_opinion",
        "date_of_purchase", "likes", "dislikes", "content"
    ]

    def __init__(self, id, author, recommendation, stars, is_opinion_confirmed_by_purchase, date_of_opinion,
                 date_of_purchase, likes, dislikes, content):
        self.features = None
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

    def setFeatures(self, features):
        for feature in features:
            feature.setOpinion(self)
        self.features = features

    def save(self):
        sql = "INSERT INTO opinions (id, product_id, author, recommendation, stars, is_opinion_confirmed_by_purchase, date_of_opinion, date_of_purchase, likes, dislikes, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        Opinion.executeQuery(sql, self.flattenObject())

        for feature in self.features:
            feature.save()

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

    @staticmethod
    def getOpinionsByProductIdForExport(productId, toObject=False):
        sql = "SELECT * FROM opinions WHERE product_id = ?"
        result = Opinion.executeQuery(sql, productId)

        return result

    @staticmethod
    def getOpinionsByProductIdForProductPage(sql):
        result = Opinion.executeQuery(sql)

        opinions = []
        for row in result:
            opinions.append(Opinion(*row))

        return opinions

    @staticmethod
    def getMetaInfoForOpinion(query, first, page):
        sql = query.select(['COUNT(*)']).construct()
        result = Opinion.executeQuery(sql)
        count = result[0][0]
        nextPage = True if count > first * page else False
        previousPage = True if page > 1 else False
        pages = math.ceil(count/first)
        return {
            'nextPage': nextPage,
            'previousPage': previousPage,
            'pages': pages,
            'count': count,
            'currentPage': page,
            'perPage': first
        }

