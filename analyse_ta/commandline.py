import analyse_ta.process_bedcov as processcov
import sys
import os
import argparse
import pkg_resources

# load config and reference files....

version = pkg_resources.require("analyse_ta")[0].version


def main():  # pragma: no cover <--
    usage = "\n %prog [options] -br input_br.bedcov -nbr input_nbr.bedcov -s <sample>"

    optParser = argparse.ArgumentParser(
        prog="analyse_ta", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    optional = optParser._action_groups.pop()
    required = optParser.add_argument_group("required arguments")

    required.add_argument(
        "-br",
        "--file_br",
        type=str,
        dest="file_br",
        required=True,
        default=None,
        help="broken ta repeat bed coverage file",
    )
    required.add_argument(
        "-nbr",
        "--file_nbr",
        type=str,
        dest="file_nbr",
        required=True,
        default=None,
        help="non broken ta repeat bed coverage file",
    )

    optional.add_argument(
        "-s",
        "--sample_name",
        type=str,
        dest="sample_name",
        required=False,
        default="test_sample",
        help="sample name",
    )

    optional.add_argument(
        "-dn",
        "--dnovo",
        action="store_true",
        dest="dnovo",
        default=False,
        help="set flag to analyse dnovo long read data",
    )

    optional.add_argument(
        "-ah",
        "--add_header",
        action="store_true",
        dest="add_header",
        default=False,
        help="set flag to add_header line, useful in batch mode to set for first sample",
    )

    optional.add_argument(
        "-dn_cutoff",
        "--dnovo_cutoff",
        type=int,
        dest="dnovo_cutoff",
        required=False,
        default=2,
        help="cut off length ratio with ref interval to flag as broken region",
    )

    optional.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + version
    )
    optional.add_argument(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        required=False,
        default=True,
    )

    optParser._action_groups.append(optional)
    if len(sys.argv) == 0:
        optParser.print_help()
        sys.exit(1)
    opts = optParser.parse_args()
    if not opts.file_nbr or not opts.file_br:
        sys.exit("\nERROR Arguments required\n\tPlease run: analyse_ta.py --help\n")
    # vars function returns __dict__ of Namespace instance
    processed = processcov.processBedCov(**vars(opts))
    print(processed.results)


if __name__ == "__main__":
    main()
