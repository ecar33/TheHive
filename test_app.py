from datetime import datetime, timedelta, timezone
import unittest
from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import Message

class WatchlistTestCase(unittest.TestCase):
    
    # Setup run before every test
    def setUp(self):
        self.app = create_app(TestingConfig)

        # Create test client and test CLI runner
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        with self.app.app_context():
            message = Message(name='test', content='test content')
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
            message.content='new content'
            self.assertEqual('new name', message.name)
            self.assertEqual('new content', message.content)

            # Test deleting a message
            db.session.delete(message)
            db.session.commit()
            message = Message.query.first()
            self.assertIsNone(message)

            # Test adding a message
            message = Message(name='test', content='test content')
            db.session.add(message)
            db.session.commit()
            self.assertEqual('test', message.name)
            self.assertEqual('test content', message.content)

    # Test message
    def test_time_since_creation(self):
        created_at_time = datetime.now(timezone.utc) - timedelta(minutes=30)
        message = Message(name='test', content='test content', created_at=created_at_time)
        result: timedelta = message.time_since_creation()
        self.assertAlmostEqual(result.total_seconds(), 30 * 60, delta=1)
    
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
            result = self.runner.invoke(args=['forge', '--num', '1'])
            self.assertIn('Messages successfully added.', result.output)
            messages = Message.query.all()
            self.assertEqual(2, len(messages))

# Run tests
if __name__ == '__main__':
    unittest.main()