class ProductsController:
    @staticmethod
    def indexProducts():
        return "Products"

    @staticmethod
    def viewProduct(id):
        return "Product " + id