from flask import render_template, send_file, redirect, request

from app.Model.Opinion import Opinion
from app.Model.Product import Product
from app.Services.ExportsHelper import ExportsHelper
from app.Services.SelectQuery import SelectQuery


class ProductsController:
    @staticmethod
    def indexProducts():
        products = Product.findProducts()

        return render_template('products/index.html', products=products)

    @staticmethod
    def viewProduct(id):
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1

        query = SelectQuery('opinions').where('product_id', '=', id).orderBy('id', 'ASC')
        paginationInfo = Opinion.getMetaInfoForOpinion(query, 10, page)
        if page > paginationInfo['pages']:
            page = 1
            paginationInfo = Opinion.getMetaInfoForOpinion(query, 10, page)

        sql = query.select(Opinion.displayFields).forPage(10, page).construct()
        opinions = Opinion.getOpinionsByProductIdForProductPage(sql)
        product = Product.findById([id])
        if not product:
            return redirect('/opinions?error=1&product_id={}'.format(id))
        return render_template(
            'products/view.html',
            fields=Opinion.displayFields,
            opinions=opinions,
            paginationInfo=paginationInfo,
            product=product
        )

    @staticmethod
    def exportOpinions(id, type):
        opinions = Opinion.getOpinionsByProductIdForExport([id])
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
