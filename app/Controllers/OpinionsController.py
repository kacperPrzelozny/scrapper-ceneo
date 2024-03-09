class OpinionsController:
    @staticmethod
    def indexOpinions():
        return "Opinions"

    @staticmethod
    def viewOpinions(productId):
        return "Opinions " + productId
