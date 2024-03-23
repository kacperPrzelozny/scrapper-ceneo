from flask import render_template, request, redirect, url_for

from app.Model.Product import Product
from app.Services.CeneoScrapperService import CeneoScrapperService


class OpinionsController:
    @staticmethod
    def indexOpinions():
        return render_template('opinions/index.html', error=False)

    @staticmethod
    def getOpinions():
        productId = request.form['productId']

        ceneoScrapper = CeneoScrapperService(productId)
        product = Product.findById([productId])

        error = None
        if product is None:
            error = ceneoScrapper.getProduct()

        if error is None:
            return redirect('/products/' + productId)

        return render_template('opinions/index.html', error=True, message=error["message"])

    @staticmethod
    def viewOpinions(productId):
        return "Opinions " + productId
