# Text Adventure
# 05-30-24
# Brian Morris

import os
import unittest
import tempfile
import shutil
import pickle
from unittest.mock import patch

import filemanager

# Test FileManager
# unit tests for file manager
class TestFileManager(unittest.TestCase):
    # initialize dummy environment
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a fake directory structure and files
        os.makedirs(os.path.join(self.test_dir, 'dir1'))
        os.makedirs(os.path.join(self.test_dir, 'dir1', 'subdir1'))
        os.makedirs(os.path.join(self.test_dir, 'dir2'))
        os.makedirs(os.path.join(self.test_dir, filemanager.SOURCE_PATH))
        os.makedirs(os.path.join(self.test_dir, filemanager.SAVES_PATH))
        
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('This is a test file.')
        
        with open(os.path.join(self.test_dir, filemanager.MAIN_SHELL), 'w') as f:
            f.write('Test main shell program.')

        with open(os.path.join(self.test_dir, filemanager.SOURCE_PATH, filemanager.ERROR_LOG), 'w') as f:
            f.write('Some vital program file.')
        
        with open(os.path.join(self.test_dir, 'dir1', 'subdir1', 'file2.txt'), 'w') as f:
            f.write('This is another test file.')

        with open(os.path.join(self.test_dir, 'dir1', 'duplicate.data'), 'w') as f:
            f.write('This file has a clone somewhere.')
        
        with open(os.path.join(self.test_dir, 'dir2', 'duplicate.data'), 'w') as f:
            f.write('This file has a clone somewhere.')
        
        with open(os.path.join(self.test_dir, filemanager.SAVES_PATH, 'save1.data'), 'wb') as f:
            pickle.dump("test string", f)
            pickle.dump(123, f)
            pickle.dump( [1, 2, 3], f)
            pickle.dump( {"key" : "value"}, f)

    # return to default environment
    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)
    
    # add log       appends given log to file, makes it if it doesn't exist
    # validate filesreturns a 1 if there is a missing dependency, and 0 if not
    # add save      returns a 1 if that save already exists, and 0 if save creation was successful
    # add config    returns 1 if there is already a config file, and 0 if file was added
    
    # test read / write / delete operations
    def test_data_manipulations(self):
        # Replace PROJECT_ROOT with self.test_dir
        with patch('filemanager.PROJECT_ROOT', self.test_dir):
            # verify read data
            result = filemanager.read_data('save1.data')
            expected = [ "test string", 123, [1, 2, 3], {"key" : "value"} ]
            self.assertEqual(result, expected)

            # verify read returns None for invalid search
            result = filemanager.read_data('fake_file.txt')
            self.assertEqual(result, None)

            # write new data
            new_data = [ {"new_key" : "new_value"} , 456, [4, 5, 6], "new string", 0 ]
            was_successful = filemanager.write_data('save1.data', new_data)
            self.assertEqual(was_successful, 0)
            # verify file now contains the new data
            self.assertEqual(filemanager.read_data('save1.data'), new_data)

            # verify write returns 1 for invalid search
            was_successful = filemanager.write_data('fake_file.txt', new_data)
            self.assertEqual(was_successful, 1)

            # delete target file
            was_successful = filemanager.delete_file('save1.data')
            self.assertEqual(was_successful, 0)
            # verify file was deleted
            self.assertEqual(filemanager.locate_file('save1.data'), None)

    # ensure file traversal behaves as expected
    def test_locate_file(self):
        # Replace PROJECT_ROOT with self.test_dr
        with patch('filemanager.PROJECT_ROOT', self.test_dir):
            # should locate one item
            result = filemanager.locate_file('file1.txt')
            expected = os.path.join(self.test_dir, 'file1.txt')
            self.assertEqual(result, expected)

            # return None because file is in FILE_DEPENDENCIES
            result = filemanager.locate_file(filemanager.MAIN_SHELL)
            self.assertEqual(result, None)

            # should locate the item in a subdirectory
            result = filemanager.locate_file('file2.txt')
            expected = os.path.join(self.test_dir, 'dir1', 'subdir1', 'file2.txt')
            self.assertEqual(result, expected)

            # return None because file is in src
            result = filemanager.locate_file('main.py')
            self.assertEqual(result, None)

            # return None because multiple matches found
            result = filemanager.locate_file('duplicate.data')
            self.assertEqual(result, None)

            # return None because no such file exists
            result = filemanager.locate_file('something.txt')
            self.assertEqual(result, None)

            # error log is found in src, but can still be edited
            result = filemanager.locate_file(filemanager.ERROR_LOG)
            expected = os.path.join(self.test_dir, filemanager.SOURCE_PATH, filemanager.ERROR_LOG)
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()