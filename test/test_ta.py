import analyse_ta.process_bedcov as processcov
import pytest
import os
import unittest.mock

'''
written test to check codebase integrity
of annotateVcf
'''

class TestClass():
  configdir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
  test_dir = configdir + '/data/'
  options = {'file_br': test_dir + 'test_br.bedcov',
                   'file_nbr': test_dir + 'test_nbr.bedcov',
                   'sample_name': 'my_test_sample',
                   }
  processed=processcov.processBedCov(**options)
  # celline output
  def test_bedcov(self):
      f=self.processed
      assert f.results == "my_test_sample\t35.23\t80.85"

