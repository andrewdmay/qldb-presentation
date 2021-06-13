import datetime
import random
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(2, 3.5)

    @task
    def send_event(self):
        event = {
            'id': random.randint(0, 99),
            'timestamp': datetime.datetime.now().isoformat(),
            'details': {
                'type': 'TEST',
                'items': [
                    {
                        'itemId': 1,
                        'description': 'An item'
                    },
                    {
                        'itemId': 2,
                        'description': 'Another'
                    }
                ],
                'changing': random.randint(0, 1000)
            }
        }

        self.client.post('/', json=event)
