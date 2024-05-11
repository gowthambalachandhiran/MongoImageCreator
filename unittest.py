import unittest
from unittest.mock import patch
from main import ServeDrawing

class TestServeDrawing(unittest.TestCase):
    def setUp(self):
        # Create a ServeDrawing instance
        self.serve_drawing = ServeDrawing()
        
        # Patch Flask app's run method to prevent actual server startup during tests
        self.serve_drawing.app.run = lambda *args, **kwargs: None

    def test_upload_file_success(self):
        # Mock request data
        request_data = {'object': 'Sun', 'session_id': '123', 'db_name': 'Nouny'}

        # Call the Flask route directly
        with self.serve_drawing.app.test_client() as client:
            response = client.post('/convert', json=request_data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('session_id', data)
        self.assertIn('file', data)

    def test_upload_file_missing_data(self):
        # Mock request data with missing 'object' key
        request_data = {'session_id': '123', 'db_name': 'Nouny'}

        # Call the Flask route directly
        with self.serve_drawing.app.test_client() as client:
            response = client.post('/convert', json=request_data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn('error', data)
        self.assertEqual(response.json['error'], "Missing data: 'object'")

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
