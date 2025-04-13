import unittest
from unittest.mock import patch
from serviceproj import app
from werkzeug.security import generate_password_hash

class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.session_transaction() as sess:
            sess.clear()

    @patch('serviceproj.views.auth.register_client')
    def test_register_success(self, mock_register_client):
        mock_register_client.return_value = True

        response = self.app.post('/register', data={
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '89991234567',
            'psw': 'password123',
            'psw_again': 'password123'
        }, follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Регистрация прошла успешно!', response_text)

    @patch('serviceproj.views.auth.register_client')
    def test_register_existing_client(self, mock_register_client):
        mock_register_client.return_value = False

        response = self.app.post('/register', data={
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '89991234567',
            'psw': 'password123',
            'psw_again': 'password123'
        }, follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Клиент с таким номером телефона уже существует', response_text)

    def test_register_password_mismatch(self):
        response = self.app.post('/register', data={
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '89991234567',
            'psw': 'password123',
            'psw_again': 'different'
        }, follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Введите одинаковые пароли', response_text)

    def test_register_missing_fields(self):
        response = self.app.post('/register', data={
            'first_name': '',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone': '89991234567',
            'psw': 'password123',
            'psw_again': 'password123'
        }, follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Заполните все поля', response_text)

if __name__ == '__main__':
    import sys
    with open("report.txt", "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner, exit=False)
