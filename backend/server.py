import json
from flask import Flask, request, jsonify
import products_dao
from sql_connection import get_sql_connection
import uom_dao
import order_dao
from analytics_dao import (
    generate_sales_report,
    generate_most_sold_products_report,
    fetch_analytics_data
)

app = Flask(__name__)
connection = get_sql_connection()

# Setting CORS for all routes
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    return add_cors_headers(response)

@app.route('/getUOM', methods=['GET'])
def get_uom():
    uom_list = uom_dao.get_uoms(connection)
    response = jsonify(uom_list)
    return add_cors_headers(response)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({'product_id': product_id})
    return add_cors_headers(response)

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    product_id = request.form['product_id']
    return_id = products_dao.delete_product(connection, product_id)
    response = jsonify({'product_id': return_id})
    return add_cors_headers(response)

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order_dao.insert_order(connection, request_payload)
    response = jsonify({'order_id': order_id})
    return add_cors_headers(response)

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    orders = order_dao.get_all_orders(connection)
    response = jsonify(orders)
    return add_cors_headers(response)

@app.route('/generate-report', methods=['GET'])
def generate_report():
    generate_sales_report()
    return jsonify({"message": "Sales report generated and displayed."})

@app.route('/generate-most-sold-products-report', methods=['GET'])
def generate_most_sold_report():
    generate_most_sold_products_report()
    return jsonify({"message": "Most sold products report generated and displayed."})


@app.route('/analytics_data', methods=['GET'])
def analytics_data():
    data = fetch_analytics_data()
    return jsonify(data.to_dict(orient='records'))


if __name__ == '__main__':
    print("Starting Python Flask Server for grocery store")
    app.run(port=5000)
