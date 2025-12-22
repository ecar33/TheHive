import unittest
from datetime import datetime, timedelta, timezone

from hive import create_app
from hive.config import TestingConfig
from hive.core.extensions import db
from hive.models import Message, User


class WatchlistTestCase(unittest.TestCase):
    # Setup run before every test
    def setUp(self):
        self.app = create_app(TestingConfig)

        # Create test client and test CLI runner
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        with self.app.app_context():
            db.create_all()
            
            message = Message(name='test', body='test body')
            user = User(username='testuser')
            password = 'password'
            user.set_password(password)
            db.session.add(message)
            db.session.add(user)
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
    
    # Test login
    def test_login(self):
        username = 'testuser'
        password = 'password'
        wrongpassword = 'abc'

        response = self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertIn(f'Successfully signed in, welcome {username}', data)

        response = self.client.post('/login', data=dict(
            username=username,
            password=wrongpassword
        ), follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertIn('User not found or password was incorrect, try again.', data)

    # Test signup
    def test_signup(self):
        username = 'testusersignup'
        password = 'password'
        wrongpassword = 'abc'

        response = self.client.post('/signup', data=dict(
            username=username,
            password=password,
            confirm_password=password
        ), follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertIn('User successfully created! Please sign in.', data)

        response = self.client.post('/signup', data=dict(
            username=username,
            password=password,
            confirm_password=password
        ), follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertIn('User already exists, please use a different username.', data)

        
        response = self.client.post('/signup', data=dict(
            username=username,
            password=password,
            confirm_password=wrongpassword
        ), follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertIn('Passwords must match.', data)
    
    # Test form
    def test_form_validation(self):
        response = self.client.post('/message/post', data=dict(
            name='test',
            body='Hello world'
        ), follow_redirects=True)
        
        assert response.status_code == 200

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

        assert response.status_code == 200

        data = response.get_data(as_text=True)
        self.assertIn('The Hive', data)
        self.assertIn('leave a message', data)
    
    # Test error pages
    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)
    
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
    
    def test_create_user(self):
        with self.app.app_context():
            # Test user is created
            username = 'test'
            password = 'password'
            result = self.runner.invoke(args=['create-user', '--username', username, '--password', password])
            
            self.assertIn('Creating user...\nDone.\n', result.output)
            
            db.session.remove() 

            user = db.session.execute(db.select(User).where(User.username == username)).scalar_one()

            self.assertIsNotNone(user)

# Run tests
if __name__ == '__main__':
    unittest.main()