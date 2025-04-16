from product_data import ProductDataGenerator
from user_behavior import UserBehaviorGenerator
import json
import time

def generate_data():
    product_gen = ProductDataGenerator()
    user_gen = UserBehaviorGenerator()
    
    while True:
        # Generate product data
        product = product_gen.generate_product()
        print(f"Generated product: {json.dumps(product, indent=2)}")
        
        # Generate user behavior
        for _ in range(random.randint(1, 5)):
            behavior = user_gen.generate_user_behavior()
            print(f"Generated user behavior: {json.dumps(behavior, indent=2)}")
            
        time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    generate_data()
