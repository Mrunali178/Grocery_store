import mysql.connector
def get_all_products():
    cnx = mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='grocery_store')  ## connection established between mysql and this code
    cursor=cnx.cursor()  #cursor will fetch the query and show the tables

    query="SELECT products.product_id,products.name,products.uom_id,products.price_per_unit,uom.uom_name FROM products inner join uom on products.uom_id=uom.uom_id;"
    cursor.execute(query)  # execute the given query
    response=[]
    for (product_id,name,uom_id,price_per_unit,uom_name) in cursor :  #this is because if not this it will print in form of tuple
        response.append({'product_id':product_id,'name':name,'uom_id':uom_id,'price_per_unit':price_per_unit,'uom_name':uom_name})
    cnx.close()  #connection closed
    return response
if __name__=='__main__':
    print(get_all_products()) 