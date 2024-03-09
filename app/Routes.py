from app.Controllers.HomeController import HomeController
from app.Controllers.OpinionsController import OpinionsController
from app.Controllers.ProductsController import ProductsController

from app.Enums.HttpMethods import HttpMethods


class Routes:
    @staticmethod
    def registerRoutes(app):
        # Home controller routes
        Routes.registerRoute(app, '/', HomeController.homePage)
        Routes.registerRoute(app, '/author', HomeController.author)

        # Opinions controller routes
        Routes.registerRoute(app, '/opinions', OpinionsController.indexOpinions)
        Routes.registerRoute(app, '/opinions/<string:productId>', OpinionsController.viewOpinions)

        # Products controller routes
        Routes.registerRoute(app, '/products', ProductsController.indexProducts)
        Routes.registerRoute(app, '/products/<string:id>', ProductsController.viewProduct)

    @staticmethod
    def registerRoute(app, path, function, methods=None):
        if methods is None:
            methods = ["GET"]

        app.add_url_rule(path, view_func=function, methods=methods)
