from app.Model.Model import Model


class Product(Model):
    def __init__(self, id, name, opinions_count, average_mark, positive_features=None, negative_features=None):
        self.opinions = None
        self.id = id
        self.name = name
        self.opinions_count = opinions_count
        self.average_mark = average_mark
        self.positive_features = positive_features
        self.negative_features = negative_features

    @staticmethod
    def findById(productId):
        sql = "SELECT * FROM products WHERE id = ?"
        result = Product.executeQuery(sql, productId)

        if len(result) != 0:
            return Product(result[0][0], result[0][1], result[0][2], result[0][3])

        return None

    def save(self):
        sql = "INSERT INTO products (id, name, opinions_count, average_mark) VALUES (?, ?, ?, ?)"
        Product.executeQuery(sql, self.flattenObject())

        for opinion in self.opinions:
            opinion.save()

    def flattenObject(self):
        return [
            self.id,
            self.name,
            self.opinions_count,
            self.average_mark
        ]

    def setOpinions(self, opinions):
        self.opinions = opinions

    @staticmethod
    def findProducts():
        sql = """
        SELECT
            products.*,
            COUNT(DISTINCT CASE WHEN features.is_positive = 1 THEN features.name END) AS positive_features,
            COUNT(DISTINCT CASE WHEN features.is_positive = 0 THEN features.name END) AS negative_features
        FROM products
        LEFT JOIN features ON features.product_id = products.id GROUP BY products.id"""
        result = Product.executeQuery(sql)

        products = []
        for row in result:
            products.append(Product(row[0], row[1], row[2], row[3], row[4], row[5]))

        return products
