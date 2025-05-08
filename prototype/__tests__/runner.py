import unittest
import os

def main():
    test_loader = unittest.TestLoader()

    # Discover all tests in the prototype directory
    test_suite = test_loader.discover(
        start_dir='prototype',
        pattern='*.test.py'
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Optional exit code logic
    if not result.wasSuccessful():
        exit(1)

if __name__ == '__main__':
    main()
