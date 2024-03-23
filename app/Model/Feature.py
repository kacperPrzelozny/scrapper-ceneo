from app.Model.Model import Model


class Feature(Model):
    def __init__(self, name, is_positive):
        self.opinion = None
        self.opinion_id = None
        self.product = None
        self.product_id = None
        self.name = name
        self.is_positive = is_positive

    def setOpinion(self, opinion):
        self.opinion = opinion
        self.opinion_id = opinion.id

    def setProduct(self, product):
        self.product = product
        self.product_id = product.id

    def save(self):
        sql = "INSERT INTO features (opinion_id, product_id, name, is_positive) VALUES (?, ?, ?, ?)"
        Feature.executeQuery(sql, self.flattenObject())

    def flattenObject(self):
        return [
            self.opinion_id,
            self.product_id,
            self.name,
            self.is_positive
        ]
