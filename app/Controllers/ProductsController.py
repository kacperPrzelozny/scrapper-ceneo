import uuid

from flask import render_template, send_file, redirect

from app.Model.Opinion import Opinion
from app.Model.Product import Product
from app.Services.ExportsHelper import ExportsHelper


class ProductsController:
    @staticmethod
    def indexProducts():
        products = Product.findProducts()

        return render_template('products/index.html', products=products)

    @staticmethod
    def viewProduct(id):
        return "Product " + id

    @staticmethod
    def exportOpinions(id, type):
        opinions = Opinion.getOpinionsByProductId([id])
        exportHelper = ExportsHelper(Opinion.fields, opinions)
        match type:
            case 'xls':
                file, filename = exportHelper.exportXls()
                file.save(filename)
                return send_file(filename, as_attachment=True)
            case 'json':
                file, filename = exportHelper.exportJson()
                return file, 200, {'Content-Type': 'text/json',
                                   'Content-Disposition': 'attachment; filename=' + filename}
            case 'csv':
                file, filename = exportHelper.exportCsv()
                return file, 200, {'Content-Type': 'text/csv',
                                   'Content-Disposition': 'attachment; filename=' + filename}
            case _:
                return redirect('/products')
