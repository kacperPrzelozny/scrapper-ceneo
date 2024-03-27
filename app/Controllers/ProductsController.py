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
        column = request.args.get('column', 'id', type=str)
        order = request.args.get('order', 'ASC', type=str)

        fieldOrders = {}
        filters = ""
        for field in Opinion.displayFields:
            fieldOrders[field] = "DESC" if column == field and order == "ASC" else "ASC"
            filters += "&" + field + "=" + request.args.get(field, '', type=str)
        filters = filters + "&"

        if page < 1:
            page = 1

        query = SelectQuery('opinions').where('product_id', '=', id).orderBy(column, order)

        query = ProductsController.applyFilters(query)

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
            fieldOrders=fieldOrders,
            opinions=opinions,
            paginationInfo=paginationInfo,
            product=product,
            column=column,
            order=order,
            r=request,
            filters=filters
        )

    @staticmethod
    def charts(id):
        p = Opinion.getDataForPieChart(id)
        pieChart = {}
        for row in p:
            r = row[1]
            if r is None:
                r = '-'
            pieChart[r] = row[0]
        b = Opinion.getDataForBarChart(id)
        barChart = {
            "0": 0, "0.5": 0, "1.0": 0, "1.5": 0, "2.0": 0, "2.5": 0, "3.0": 0, "3.5": 0, "4.0": 0, "4.5": 0, "5.0": 0,
        }
        for row in b:
            barChart[str(row[1])] = row[0]
        print(barChart)
        return render_template('products/charts.html', pieChart=pieChart, barChart=barChart, id=id)

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

    @staticmethod
    def applyFilters(query):
        author = request.args.get('author', '', type=str)
        if author != "":
            query.where("author", "LIKE", "'%" + author + "%'")

        recommendation = request.args.get('recommendation', "", type=str)
        if recommendation != "" and recommendation != "-":
            query.where("recommendation", "LIKE", "'%" + request.args.get('recommendation', "", type=str) + "%'")
        if recommendation == "-":
            query.where("recommendation", "IS", "NULL")

        is_opinion_confirmed_by_purchase = request.args.get('is_opinion_confirmed_by_purchase', "", type=str)
        if is_opinion_confirmed_by_purchase != '':
            query.where("is_opinion_confirmed_by_purchase", "LIKE",
                        "'%" + request.args.get('is_opinion_confirmed_by_purchase', "", type=str) + "%'")

        date_of_opinion = request.args.get('date_of_opinion', "", type=str)
        if date_of_opinion != "":
            query.where("date_of_opinion", "LIKE", "'%" + date_of_opinion + "%'")

        date_of_purchase = request.args.get('date_of_purchase', "", type=str)
        if date_of_purchase != "":
            query.where("date_of_purchase", "LIKE", "'%" + date_of_purchase + "%'")

        likes = request.args.get('likes', -1, type=int)
        if likes != -1:
            query.where("likes", "=", likes)

        dislikes = request.args.get('dislikes', -1, type=int)
        if dislikes != -1:
            query.where("dislikes", "=", dislikes)

        stars = request.args.get('stars', '', type=str)
        if stars != "":
            query.where("stars", "=", stars)

        content = request.args.get('content', "", type=str)
        if content != "":
            query.where("content", "LIKE", "'%" + content + "%'")

        return query
