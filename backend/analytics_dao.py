import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sql_connection import get_sql_connection

def fetch_analytics_data():
    """Fetch daily sales and order data from the database."""
    connection = get_sql_connection()
    cursor = connection.cursor()

    query = """
    SELECT DATE(datetime) as date, SUM(total) as total_sales, COUNT(order_id) as total_orders
    FROM orders
    GROUP BY DATE(datetime)
    ORDER BY DATE(datetime);
    """
    cursor.execute(query)
    result = cursor.fetchall()

    data = pd.DataFrame(result, columns=['date', 'total_sales', 'total_orders'])
    data['date'] = pd.to_datetime(data['date'])
    return data

def fetch_most_sold_products():
    """Fetch the most sold products along with their details."""
    connection = get_sql_connection()
    cursor = connection.cursor()
    
    query = """
    SELECT p.product_id, p.name AS product_name, SUM(od.quantity) as total_quantity, AVG(od.total_price) as average_price
    FROM order_details od
    JOIN products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.name
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    
    products_data = pd.DataFrame(result, columns=['product_id', 'product_name', 'total_quantity', 'average_price'])
    return products_data

def generate_sales_report():
    """Generate and display the sales report."""
    data = fetch_analytics_data()
    summary_report = data.describe()
    print("Sales Summary Report:")
    print(summary_report)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='date', y='total_sales', label='Total Sales', color='blue')
    sns.lineplot(data=data, x='date', y='total_orders', label='Total Orders', color='orange')
    plt.title('Daily Sales and Orders')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def generate_most_sold_products_report():
    """Generate and display the report of most sold products."""
    products_data = fetch_most_sold_products()
    
    print("Most Sold Products Report:")
    print(products_data)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=products_data, x='product_name', y='total_quantity', palette='viridis')
    plt.title('Most Sold Products')
    plt.xlabel('Product Name')
    plt.ylabel('Total Quantity Sold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # You can also create a function to run both reports
    print("Generating Reports...")
    generate_sales_report()
    generate_most_sold_products_report()
    print("Reports generated successfully!")
