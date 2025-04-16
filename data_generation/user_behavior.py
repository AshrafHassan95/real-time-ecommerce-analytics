import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

class UserBehaviorGenerator:
    def __init__(self):
        self.events = ['page_view', 'add_to_cart', 'purchase', 'product_click']
        
    def generate_user_behavior(self, user_id=None):
        user_id = user_id or fake.uuid4()
        return {
            'event_id': fake.uuid4(),
            'user_id': user_id,
            'event_type': random.choice(self.events),
            'timestamp': datetime.now().isoformat(),
            'session_id': fake.uuid4(),
            'device': random.choice(['mobile', 'desktop', 'tablet']),
            'location': fake.country_code()
        }
