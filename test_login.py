import unittest
from flask import session
from app import create_app

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    # Test Case - Login as System Admin
    def test_login_sysadmin_valid_credentials(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/login', data=dict(
                username='admin1',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'ViewNest Dashboard', response.data)

    # Test Case - Login as System Admin (Invalid Username)
    def test_login_sysadmin_incorrect_username(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='WrongUsernameSysAdmin',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Login as System Admin (Invalid Password)
    def test_login_sysadmin_incorrect_password(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='admin1',
                password='WrongPassword!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Logout as Sysadmin
    def test_logout_sysadmin(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'ViewNest Dashboard', response.data)  # Check if redirected to login page

    # Test Case - Login as REA 
    def test_login_REA_credentials(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/login', data=dict(
                username='rea1',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'ViewNest Dashboard', response.data)

    # Test Case - Login as REA (Invalid Username)
    def test_login_REA_incorrect_username(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='WrongUsernameREA',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Login as REA (Invalid Password)
    def test_login_REA_incorrect_password(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='rea1',
                password='WrongPassword!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Logout as REA
    def test_logout_REA(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'ViewNest Dashboard', response.data)  # Check if redirected to login page

   # Test Case - Login as Buyer 
    def test_login_buyer_valid_credentials(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/login', data=dict(
                username='buyer',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'ViewNest Dashboard', response.data)

    # Test Case - Login as Buyer (Invalid Username)
    def test_login_buyer_incorrect_username(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='WrongUsernameBuyer',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Login as Buyer (Invalid Password)
    def test_login_buyer_incorrect_password(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='buyer',
                password='WrongPassword!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Logout as Buyer
    def test_logout_buyer(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'ViewNest Dashboard', response.data)  # Check if redirected to login page


   # Test Case - Login as Seller 
    def test_login_seller_valid_credentials(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/login', data=dict(
                username='sell',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'ViewNest Dashboard', response.data)

    # Test Case - Login as Seller (Invalid Username)
    def test_login_seller_incorrect_username(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='WrongUsernameSeller',
                password='Password1!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Login as Seller (Invalid Password)
    def test_login_seller_incorrect_password(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username='sell',
                password='WrongPassword!'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect username or password. Please try again.', response.data)

    # Test Case - Logout as Seller
    def test_logout_seller(self):
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # Mocking user session
            response = client.post('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'ViewNest Dashboard', response.data)  # Check if redirected to login page


if __name__ == '__main__':
    unittest.main()
