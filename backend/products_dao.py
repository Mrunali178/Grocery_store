from sql_connection import get_sql_connection
def get_all_products(connection):

    cursor=connection.cursor()  #cursor will fetch the query and show the tables

    query="SELECT products.product_id,products.name,products.uom_id,products.price_per_unit,uom.uom_name FROM products inner join uom on products.uom_id=uom.uom_id;"
    cursor.execute(query)  # execute the given query
    response=[]
    for (product_id,name,uom_id,price_per_unit,uom_name) in cursor :  #this is because if not this it will print in form of tuple
        response.append({'product_id':product_id,'name':name,'uom_id':uom_id,'price_per_unit':price_per_unit,'uom_name':uom_name})
    return response

def insert_new_product(connection,product):
    cursor=connection.cursor()
    query=("insert into products(name,uom_id,price_per_unit) values (%s,%s,%s)")
    data=(product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query,data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection,product_id):
    cursor=connection.cursor()
    query=("delete from products where product_id = "+ str(product_id))
    cursor.execute(query)
    connection.commit()

if __name__=='__main__':
    connection=get_sql_connection()
    print(delete_product(connection,10)) 