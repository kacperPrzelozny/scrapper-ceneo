from flask import render_template


class OpinionsController:
    @staticmethod
    def indexOpinions():
        return render_template('opinions/index.html')
    @staticmethod
    def viewOpinions(productId):
        return "Opinions " + productId
