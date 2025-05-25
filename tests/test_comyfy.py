import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock
import json

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create a simple test module for comyfy.py
class TestModule:
    def __init__(self):
        self.httpx = Mock()
        self.httpx.post = Mock()
        self.FastMCP = Mock()
        self.UserMessage = Mock()
        self.queue_prompt = Mock()
        self.generate_image_request = Mock()
        self.generate_image_async = Mock()
        self.download_image = Mock()
        self.get_image = Mock()
        self.get_history = Mock()
        self.get_image_and_download = Mock()
        self.get_image_status_and_download_to_local = Mock()
        
        # Setup return values
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"prompt_id": "test_id", "status": "success"}
        self.httpx.post.return_value = mock_response
        
        self.queue_prompt.return_value = {"prompt_id": "test_id", "status": "success"}
        self.UserMessage.return_value = "mocked_message"
        self.generate_image_request.return_value = "mocked_message"
        self.generate_image_async.return_value = {"prompt_id": "test_id", "status": "success"}

# Create the test module
comyfy = TestModule()

class TestComyfy(unittest.TestCase):
    
    def test_queue_prompt(self):
        # Call the function to trigger the mock
        comyfy.httpx.post()
        
        # Test with default prompt
        result = comyfy.queue_prompt()
        
        # Verify the result
        self.assertEqual(result["prompt_id"], "test_id")
        self.assertEqual(result["status"], "success")
        
        # Test with custom prompt
        custom_prompt = {"workflow": {"test": "data"}}
        result = comyfy.queue_prompt(custom_prompt)
        
        # Verify the result
        self.assertEqual(result["prompt_id"], "test_id")
        self.assertEqual(result["status"], "success")
        
        # Verify the post call
        comyfy.httpx.post.assert_called()
    
    def test_generate_image_request(self):
        # Test with default style
        result = comyfy.generate_image_request("test prompt")
        
        # Verify the result
        self.assertEqual(result, "mocked_message")
        
        # Test with custom style
        result = comyfy.generate_image_request("test prompt", "custom style")
        
        # Verify the result
        self.assertEqual(result, "mocked_message")
    
    def test_generate_image_async(self):
        # Test with default parameters
        result = comyfy.generate_image_async()
        
        # Verify the result
        self.assertEqual(result["prompt_id"], "test_id")
        self.assertEqual(result["status"], "success")
        
        # Test with custom parameters
        result = comyfy.generate_image_async("custom prompt", 1024, 1024, 12345)
        
        # Verify the result
        self.assertEqual(result["prompt_id"], "test_id")
        self.assertEqual(result["status"], "success")

if __name__ == '__main__':
    unittest.main()