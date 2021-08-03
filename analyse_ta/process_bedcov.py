import os
import sys
import pandas as pd


'''
  This class claculates mean coverage for broken and non_broken TA reapeat depth output fron samtools bedcov
'''


class processBedCov:
    """
        Main class , loads user defined parameters and files
    """

    def __init__(self, **kwargs):
        self.br_file = kwargs['file_br']
        self.nbr_file = kwargs['file_nbr']
        self.sample = kwargs.get('sample_name', 'test_sample')
        # check input data ...
        self.results = self.process()

    def process(self):
        mydf_br = create_df_to_merge(self.br_file, 'br')
        mydf_nbr = create_df_to_merge(self.nbr_file, 'nbr')
        merged_df = pd.concat([mydf_nbr, mydf_br])
        mean_fpmb_const = merged_df['frl'].sum(axis=0)
        merged_df['fpbm'] = merged_df['frl'] / mean_fpmb_const * (10**6)
        br_mean = merged_df.loc[merged_df.ta_type == 'br']
        nbr_mean = merged_df.loc[merged_df.ta_type == 'nbr']
        return f"{self.sample}\t{br_mean['fpbm'].mean(axis=0):.2f}\t{nbr_mean['fpbm'].mean(axis=0):.2f}"


def create_df_to_merge(infile, ta_type):
    """
       create pandas data frame
    """
    if not os.path.isfile(infile):
        return None
    df = pd.read_csv(infile, compression='infer', sep="\t", low_memory=False,
                     header=None, names=['chr', 'start', 'end', 'coverage'])
    df['frl'] = df['coverage'] / (df['end'] - df['start']) + 1
    df['ta_type'] = ta_type
    return df
