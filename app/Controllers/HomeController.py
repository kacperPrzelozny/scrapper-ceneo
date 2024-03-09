from flask import render_template


class HomeController:
    @staticmethod
    def homePage():
        return render_template('home/homePage.html')

    @staticmethod
    def author():
        return "Author page"
