from app.Model.Model import Model


class Product(Model):
    def __init__(self, id, name, opinions_count, average_mark):
        self.id = id
        self.name = name
        self.opinions_count = opinions_count
        self.average_mark = average_mark

    @staticmethod
    def findById(id):
        sql = "SELECT * FROM products WHERE id = ?"
        result = Product.executeQuery(sql, id)

        if len(result) != 0:
            return Product(result[0][0], result[0][1], result[0][2], result[0][3])

        return None

    def save(self):
        sql = "INSERT INTO products (id, name, opinions_count, average_mark) VALUES (?, ?, ?, ?)"
        Product.executeQuery(sql, self.flattenObject())

    def flattenObject(self):
        return [self.id, self.name, self.opinions_count, self.average_mark]
