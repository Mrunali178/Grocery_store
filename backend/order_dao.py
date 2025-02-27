from datetime import datetime
from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    # print(order)
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(customer_name, total, datetime)"
             "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid
    # print("Order ID:", order_id)
    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append((
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ))
    # print(order_details_data)
    # print(order_details_query)
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    
    return response


if __name__=="__main__":
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(insert_order(connection, {
    #     'customer_name': 'atharav',
    #     'total': '300',
    #     'order_details': [
    #         {'product_id': 1, 'quantity': 2, 'total_price': 50},
    #         {'product_id': 2, 'quantity': 2, 'total_price': 60}
    #     ]
    # }))