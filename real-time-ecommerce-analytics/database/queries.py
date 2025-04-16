import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseQueries:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database='ecommerce_analytics'
        )
        
    def insert_product(self, product_data):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO products 
            (product_id, name, category, price, rating, stock, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            product_data['product_id'],
            product_data['name'],
            product_data['category'],
            product_data['price'],
            product_data['rating'],
            product_data['stock'],
            product_data['created_at']
        ))
        self.conn.commit()
        cursor.close()
        
    def insert_user_behavior(self, behavior_data):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO user_behavior
            (event_id, user_id, event_type, timestamp, session_id, device, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            behavior_data['event_id'],
            behavior_data['user_id'],
            behavior_data['event_type'],
            behavior_data['timestamp'],
            behavior_data['session_id'],
            behavior_data['device'],
            behavior_data['location']
        ))
        self.conn.commit()
        cursor.close()
        
    def get_popular_products(self, limit=10):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT p.product_id, p.name, p.category, COUNT(ub.event_id) as interactions
            FROM products p
            JOIN user_behavior ub ON p.product_id = ub.product_id
            GROUP BY p.product_id
            ORDER BY interactions DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()
        cursor.close()
        return result
        
    def __del__(self):
        self.conn.close()
