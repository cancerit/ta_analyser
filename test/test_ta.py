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
                   'dnovo':False,
                   'add_header':True,
                   'dnovo_cutoff':2,
                   'sample_name': 'my_test_sample',
                   }
  options_ta_ext = {'file_br': test_dir + 'test_br.bedcov',
                   'file_nbr': test_dir + 'test_nbr.bedcov',
                   'dnovo':True,
                   'add_header':False,
                   'dnovo_cutoff':10,
                   'sample_name': 'my_test_sample',
                   }
  processed=processcov.processBedCov(**options)
  processed_ta_ext=processcov.processBedCov(**options_ta_ext)
  # celline output
  def test_bedcov(self):
      f=self.processed
      assert f.results == "sample\tfpbm_br\tfpbm_nbr\nmy_test_sample\t33.04\t82.05"
  
  def test_ta_ext(self):
      f_ext=self.processed_ta_ext
      assert f_ext.results == "my_test_sample\t33.04\t82.05\t5434\t10000\t79.39\t14.36\t11970\t3464\t2776\t806\t67.53\t67.78\t18.98\t6.37"

