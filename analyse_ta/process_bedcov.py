import os
import sys
import pandas as pd
import numpy as np


"""
  This class claculates mean coverage for broken and non_broken TA reapeat depth output fron samtools bedcov
"""


class processBedCov:
    """
    Main class , loads user defined parameters and files
    """

    def __init__(self, **kwargs):
        self.br_file = kwargs["file_br"]
        self.nbr_file = kwargs["file_nbr"]
        self.dnovo = kwargs["dnovo"]
        self.add_header = kwargs["add_header"]
        self.dnovo_cutoff = kwargs["dnovo_cutoff"]
        self.sample = kwargs.get("sample_name", "test_sample")
        # check input data ...
        self.results = self.process()

    def process(self):
        mydf_br = create_df_to_merge(self.br_file, "br", self.dnovo_cutoff, self.dnovo)
        mydf_nbr = create_df_to_merge(
            self.nbr_file, "nbr", self.dnovo_cutoff, self.dnovo
        )
        merged_df = pd.concat([mydf_nbr, mydf_br])
        mean_fpmb_const = merged_df["frl"].sum(axis=0)
        merged_df["fpbm"] = merged_df["frl"] / mean_fpmb_const * (10**6)
        br_mean = merged_df.loc[merged_df.ta_type == "br"]
        nbr_mean = merged_df.loc[merged_df.ta_type == "nbr"]
        header = f"sample\tfpbm_br\tfpbm_nbr\n"
        output = ""
        if self.add_header:
            output = header
        if self.dnovo:
            if self.add_header:
                output = output.strip()
                output = (f"{output}\tref_br\tref_nbr\tmean_fpbm_dnovo_br\tmean_fpbm_dnovo_br\tdnovo_br\tdnovo_nbr"
                         f"\tdnovo_in_ref_br\tdnovo_in_ref_nbr\tcumulative_fpbm_br"
                         f"\tcumulative_fpbm_nbr\tjaccard_br\tjaccard_nbr\n")
            br_mean_dnovo = merged_df.loc[merged_df.ta_type_dnovo == "br"]
            nbr_mean_dnovo = merged_df.loc[merged_df.ta_type_dnovo == "nbr"]
            br_cumulative_mean = merged_df.loc[
                (merged_df["ta_type_dnovo"] == "br") | (merged_df["ta_type"] == "br")
            ]
            nbr_cumulative_mean = merged_df.loc[
                (merged_df["ta_type_dnovo"] == "nbr") | (merged_df["ta_type"] == "nbr")
            ]
            num_br = len(merged_df[merged_df["ta_type"] == "br"])
            num_nbr = len(merged_df[merged_df["ta_type"] == "nbr"])
            num_br_dnovo = len(merged_df[merged_df["ta_type_dnovo"] == "br"])
            num_nbr_dnovo = len(merged_df[merged_df["ta_type_dnovo"] == "nbr"])
            br_m11 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] == "br") & (merged_df["ta_type"] == "br")
                ]
            )
            br_m01 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] != "br") & (merged_df["ta_type"] == "br")
                ]
            )
            br_m10 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] == "br") & (merged_df["ta_type"] != "br")
                ]
            )
            nbr_m11 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] == "nbr") & (merged_df["ta_type"] == "nbr")
                ]
            )
            nbr_m01 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] != "nbr") & (merged_df["ta_type"] == "nbr")
                ]
            )
            nbr_m10 = len(
                merged_df[
                    (merged_df["ta_type_dnovo"] == "nbr") & (merged_df["ta_type"] != "nbr")
                ]
            )

            jindex_br = (br_m11 / (br_m01 + br_m10 + br_m11)) * 100
            jindex_nbr = (nbr_m11 / (nbr_m01 + nbr_m10 + nbr_m11)) * 100

            return (
                f"{output}{self.sample}\t{br_mean['fpbm'].mean(axis=0):.2f}"
                f"\t{nbr_mean['fpbm'].mean(axis=0):.2f}\t{num_br}\t{num_nbr}"
                f"\t{br_mean_dnovo['fpbm'].mean(axis=0):.2f}\t{nbr_mean_dnovo['fpbm'].mean(axis=0):.2f}"
                f"\t{num_br_dnovo}\t{num_nbr_dnovo}\t{br_m11}\t{nbr_m11}"
                f"\t{br_cumulative_mean['fpbm'].mean(axis=0):.2f}"
                f"\t{nbr_cumulative_mean['fpbm'].mean(axis=0):.2f}\t{jindex_br:.2f}\t{jindex_nbr:.2f}"
            )

        output = f"{output}{self.sample}\t{br_mean['fpbm'].mean(axis=0):.2f}\t{nbr_mean['fpbm'].mean(axis=0):.2f}"
        return output


def create_df_to_merge(infile, ta_type, dnovo_cutoff, dnovo=None):
    """
    create pandas data frame
    """
    if not os.path.isfile(infile):
        print(f"File not found {infile}")
        return None
    df = pd.read_csv(
        infile,
        compression="infer",
        sep="\t",
        low_memory=False,
        header=None,
        names=["chr", "start", "end", "coverage"],
    )

    if dnovo:
        df["frl"] = (df["coverage"] * 2) / ((df["end"] - df["start"]) + 1)
        df["ta_type_dnovo"] = np.select(
            [df["frl"] <= dnovo_cutoff, df["frl"] > dnovo_cutoff], ["nbr", "br"]
        )
        df["ta_type"] = ta_type

    else:
        df["frl"] = df["coverage"] / ((df["end"] - df["start"]) + 1)
        df["ta_type"] = ta_type
    return df


def _print_df(mydf, out_file):
    if out_file:
        mydf.to_csv(
            out_file, sep="\t", mode="w", header=True, index=True, doublequote=False
        )
    else:
        sys.exit("Outfile not provided")
