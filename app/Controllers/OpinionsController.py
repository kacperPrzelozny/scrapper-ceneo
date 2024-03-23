
from flask import render_template, request

from app.Model.Product import Product
from app.Services.CeneoScrapperService import CeneoScrapperService


class OpinionsController:
    @staticmethod
    def indexOpinions():
        return render_template('opinions/index.html')

    @staticmethod
    def getOpinions():
        productId = request.form['productId']

        ceneoScrapper = CeneoScrapperService(productId)
        product = Product.findById([productId])

        if product is None:
            product = ceneoScrapper.getProduct()



        return render_template('opinions/index.html')

    @staticmethod
    def viewOpinions(productId):
        return "Opinions " + productId
