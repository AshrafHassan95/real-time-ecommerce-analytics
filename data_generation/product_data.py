import random
from faker import Faker

fake = Faker()

class ProductDataGenerator:
    def __init__(self):
        self.categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
        
    def generate_product(self):
        return {
            'product_id': fake.uuid4(),
            'name': fake.bs(),
            'category': random.choice(self.categories),
            'price': round(random.uniform(10, 1000), 2),
            'rating': round(random.uniform(1, 5), 1),
            'stock': random.randint(0, 1000),
            'created_at': fake.date_time_this_year().isoformat()
        }
