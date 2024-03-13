from flask import render_template


class ProductsController:
    @staticmethod
    def indexProducts():
        return render_template('products/index.html')

    @staticmethod
    def viewProduct(id):
        return "Product " + id