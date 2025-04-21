import google.generativeai as genai
import pymysql
from dotenv import load_dotenv
import os
import random
import time
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

def validate_env_vars(*vars):
    """Validate required environment variables"""
    for var in vars:
        if not os.getenv(var):
            logger.error(f"Environment variable {var} is not set")
            raise ValueError(f"{var} is required")

def initialize_genai():
    """Initialize Google GenAI with proper authentication"""
    validate_env_vars('GENAI_API_KEY')
    api_key = os.getenv('GENAI_API_KEY')
    
    try:
        genai.configure(api_key=api_key)
        logger.info("Successfully configured Google GenAI")
        return genai.GenerativeModel('gemini-1.5-pro-002')
    except Exception as e:
        logger.error(f"Failed to initialize GenAI: {e}")
        raise

def get_random_product():
    """Retrieve a random product from database"""
    validate_env_vars('MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE')
    
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT product_id, name, category 
                FROM products 
                ORDER BY RAND() 
                LIMIT 1
            """)
            result = cursor.fetchone()
            if result:
                logger.info(f"Fetched product: {result['name']} (ID: {result['product_id']})")
            return (result['product_id'], result['name'], result['category']) if result else None
            
    except pymysql.MySQLError as e:
        logger.error(f"Database error: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def generate_insight(model, product_id, product_name, category):
    """Generate AI insight for a product"""
    prompt = f"""
    Generate a concise marketing insight (2-3 sentences) about:
    Product: {product_name}
    Category: {category}

    The insight should:
    - Highlight customer appeal
    - Suggest marketing angles
    - Be actionable and specific
    - Use professional but engaging language
    """
    
    try:
        response = model.generate_content(prompt)
        logger.info(f"Generated insight for product ID {product_id}")
        return response.text
    except Exception as e:
        logger.error(f"AI generation failed for product ID {product_id}: {e}")
        return None

def store_insight(product_id, insight_text):
    """Store insight in database"""
    if not insight_text:
        logger.warning(f"No insight text provided for product ID {product_id}")
        return False
        
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ai_insights (product_id, insight_text)
                VALUES (%s, %s)
            """, (product_id, insight_text))
            connection.commit()
            logger.info(f"Stored insight for product ID {product_id}")
            return True
            
    except pymysql.MySQLError as e:
        logger.error(f"Failed to store insight for product ID {product_id}: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

def main():
    """Main execution loop"""
    try:
        model = initialize_genai()
    except ValueError as e:
        logger.error(f"Initialization failed: {e}")
        return
    
    while True:
        try:
            # Get random product
            product_info = get_random_product()
            if not product_info:
                logger.warning("No products found in database")
                time.sleep(60)
                continue
                
            product_id, product_name, category = product_info
            
            # Generate insight
            insight_text = generate_insight(model, product_id, product_name, category)
            if not insight_text:
                time.sleep(60)  # Wait longer after failures
                continue
                
            # Store insight
            if store_insight(product_id, insight_text):
                logger.info(f"Generated and stored insight for {product_name}")
            else:
                logger.warning(f"Failed to store insight for {product_name}")
                
            # Random delay between 1-5 minutes
            time.sleep(random.randint(60, 300))
            
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()