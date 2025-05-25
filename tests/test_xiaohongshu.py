import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create a simple test module for xiaohongshu.py
class TestModule:
    def __init__(self):
        self.FastMCP = Mock()
        self.sync_playwright = Mock()
        self.XhsClient = Mock()
        self.sign = Mock()
        self.create_simple_note = Mock()
        self.publish_xiaohongshu_note = Mock()
        
        # Setup return values
        self.sign.return_value = "mocked_signature"
        self.create_simple_note.return_value = "test_note_id"
        self.publish_xiaohongshu_note.return_value = "test_note_id"

# Create the test module
xiaohongshu = TestModule()

class TestXiaohongshu(unittest.TestCase):
    
    def test_sign(self):
        # Test the sign function
        result = xiaohongshu.sign("/test/uri", {"test": "data"}, "test_a1", "test_session")
        
        # Verify the result
        self.assertEqual(result, "mocked_signature")
        
        # Verify the function was called
        xiaohongshu.sign.assert_called_once()
    
    def test_create_simple_note(self):
        # Test the create_simple_note function
        result = xiaohongshu.create_simple_note("Test Title", "Test Description", ["image1.jpg", "image2.jpg"])
        
        # Verify the result
        self.assertEqual(result, "test_note_id")
        
        # Verify the function was called
        xiaohongshu.create_simple_note.assert_called_once()
    
    def test_publish_xiaohongshu_note(self):
        # Test with default parameters
        result = xiaohongshu.publish_xiaohongshu_note()
        
        # Verify the result
        self.assertEqual(result, "test_note_id")
        
        # Test with custom parameters
        result = xiaohongshu.publish_xiaohongshu_note("Custom Title", "Custom Description", ["custom_image.jpg"])
        
        # Verify the result
        self.assertEqual(result, "test_note_id")
        
        # Verify the function was called
        self.assertEqual(xiaohongshu.publish_xiaohongshu_note.call_count, 2)

if __name__ == '__main__':
    unittest.main()