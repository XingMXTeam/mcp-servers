# Tests for MCP Servers

This directory contains unit tests for the MCP Servers project.

## Running Tests

To run all tests, use the following command from the project root directory:

```bash
python tests/run_tests.py
```

## Test Structure

The tests are organized by module:

- `test_comyfy.py`: Tests for the `comyfy.py` module
- `test_xiaohongshu.py`: Tests for the `xiaohongshu.py` module

## Adding New Tests

When adding new tests:

1. Follow the existing pattern of using unittest
2. Use mocks for external dependencies
3. Add your test class to the appropriate test file or create a new one if needed
4. Make sure your tests are isolated and don't depend on external services

## Dependencies

The tests require the following Python packages:

- unittest (standard library)
- mock (standard library in Python 3)

Plus all the dependencies required by the main application.