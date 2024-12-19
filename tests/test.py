from datetime import datetime, timedelta, timezone
import unittest
from hive import create_app
from hive.config import TestingConfig
from hive.core.extensions import db
from hive.models import Message

class WatchlistTestCase(unittest.TestCase):
    
    # Setup run before every test
    def setUp(self):
        self.app = create_app(TestingConfig)

        # Create test client and test CLI runner
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        with self.app.app_context():
            message = Message(name='test', body='test body')
            db.session.add(message)
            db.session.commit()

    # Cleanup run after every test
    def tearDown(self):
        with self.app.test_request_context():
            db.drop_all()
            db.session.close()
            db.session.remove()
    
    # Testing app creation
    def test_app_exist(self):
        self.assertIsNotNone(self.app)
    
    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])
    
    # Test db
    def test_message(self):
        with self.app.app_context():

            # Test message was succesfully added
            message = Message.query.first()
            self.assertTrue(message)
            
            # Test modifying message
            message.name='new name'
            message.body='new body'
            self.assertEqual('new name', message.name)
            self.assertEqual('new body', message.body)

            # Test deleting a message
            db.session.delete(message)
            db.session.commit()
            message = Message.query.first()
            self.assertIsNone(message)

            # Test adding a message
            message = Message(name='test', body='test body')
            db.session.add(message)
            db.session.commit()
            self.assertEqual('test', message.name)
            self.assertEqual('test body', message.body)

    # Test message
    def test_time_since_creation(self):
        created_at_time = datetime.now(timezone.utc) - timedelta(minutes=30)
        message = Message(name='test', body='test body', created_at=created_at_time)
        result: timedelta = message.time_since_creation()
        self.assertAlmostEqual(result.total_seconds(), 30 * 60, delta=1)
    
    # Test form
    def test_form_validation(self):
        response = self.client.post('/message/post', data=dict(
            name='test',
            body='Hello world'
        ), follow_redirects=True)

        data = response.get_data(as_text=True)
        self.assertIn('Message succesfully added!', data)
        self.assertIn('Hello world', data)

        response = self.client.post('/message/post', data=dict(
            name='',
            body='Bad form'
        ), follow_redirects=True)

        data = response.get_data(as_text=True)
        self.assertIn('Error in message', data)
        self.assertNotIn('Bad form', data)

    # Test index page
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('')

    # Test CLI
    def test_initdb(self):
        with self.app.app_context():
            # Test db initializes
            result = self.runner.invoke(args=['initdb'])
            self.assertIn('Initialized database.', result.output)

            # Test db drops and initializes
            result = self.runner.invoke(args=['initdb', '--drop'])
            self.assertIn('Database dropped.', result.output)
            self.assertIn('Initialized database.', result.output)
    
    def test_forge(self):
        with self.app.app_context():
            # Test db initializes
            count = 10
            result = self.runner.invoke(args=['forge', '--num', count])
            self.assertIn(f'{count} messages successfully added.', result.output)
            messages = Message.query.all()

            # DB starts with 1 message, so check for count + 1 messages
            self.assertEqual(11, len(messages))
    
# Run tests
if __name__ == '__main__':
    unittest.main()