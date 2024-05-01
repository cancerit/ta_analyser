# ta_analyser
[![cancerit](https://circleci.com/gh/cancerit/ta_analyser.svg?style=svg)](https://circleci.com/gh/cancerit/ta_analyser)

This project hosts script to calculate mean FPBM (fragments per base per million) values for TA repeats using samtools bedcov output 
For detailed description on method to calculate the FPBM values please refer [Nature] article.


`samtools bedcov analyse_ta/data/liftover_broken_ta_sorted_fai.bed.gz test.bam >test_br.bedcov` 
`samtools bedcov analyse_ta/data/liftover_non_broken_ta_sorted_fai.bed.gz test.bam >test_nbr.bedcov`

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Design](#design)
- [Tools](#tools)
	- [analyse_ta](#analyse_ta)
	- [inputFormat](#inputformat)
	- [outputFormat](#outputformat)
- [INSTALL](#install)
	- [Package Dependencies](#package-dependencies)
- [Development environment](#development-environment)
	- [Development Dependencies](#development-dependencies)
		- [Setup VirtualEnv](#setup-virtualenv)
- [Cutting a release](#cutting-a-release)
	- [Install via `.whl` (wheel)](#install-via-whl-wheel)
- [Reference](#reference)

<!-- /TOC -->

## Design

Uses pandas>=1.3.1

## Tools

`analyse_ta` has multiple command line options, listed with `analyse_ta --help`.

### analyse_ta
Takes samtools bed coverage as input file for broken and non-broken ta repeat intervals and optional sample_name parameter.

Various exceptions can occur for malformed input files.

### inputFormat

 * ```test_br.bedcov```  bed coverage file for broken TA repeats generated using [samtools]
 * ```test_nbr.bedcov```  bed coverage file for non-broken TA repeats generated using [samtools]
 * ```test_sample```  sample name to be printed with results

### outputFormat

 * ```test_sample 6.12 15.8``` command line output <sample_name> <mean_fpbm_broken> <mean_fpbm_non_broken>.

### outputFormat with dnovo flag set 
* ```Applicable only to Long Read sequencing data ```
Use of dnovo flag will classify the TA repeat regions into broken and non-broken based on the user defined dnovo_cutoff parmater.
This  is applicable for long read data where average length of TA repeat is known for each interval
* ```br:broken```
* ```nbr:non_broken```
* ```test_sample 6.12 15.8``` command line output <sample_name> <mean_fpbm_br> <mean_fpbm_nbr> <ref_br> <ref_nbr> <mean_fpbm_dnovo_br> <mean_fpbm_dnovo_br> <dnovo_br> <dnovo_nbr> <dnovo_in_ref_br> <dnovo_in_ref_nbr> <cumulative_fpbm_br> <cumulative_fpbm_nbr> <jaccard_br> <jaccard_nbr>. 

## INSTALL
Installing via `pip install`. Simply execute with the path to the compiled 'whl' found on the [release page][analyse_ta-releases]:

```bash
python3 setup.py sdist bdist_wheel
pip install analyse_ta.X.X.X-py3-none-any.whl
```

Release `.whl` files are generated as part of the release process and can be found on the [release page][analyse_ta-releases]

## Development environment

This project uses git pre-commit hooks.  As these will execute on your system it
is entirely up to you if you activate them.

If you want tests, coverage reports and lint-ing to automatically execute before
a commit you can activate them by running:

```
git config core.hooksPath git-hooks
```

Only a test failure will block a commit, lint-ing is not enforced (but please consider
following the guidance).

You can run the same checks manually without a commit by executing the following
in the base of the clone:

```bash
./run_tests.sh
```

### Development Dependencies

pytest
radon
pytest-cov

#### Setup VirtualEnv

```
cd $PROJECTROOT
hash virtualenv || pip3 install virtualenv
virtualenv -p python3 env
source env/bin/activate
python setup.py develop # so bin scripts can find module
```

For testing/coverage (`./run_tests.sh`)

```
source env/bin/activate # if not already in env
pip install pytest
pip install radon
pip install pytest-cov
```

__Also see__ [Package Dependancies](#package-dependancies)

### Cutting a release

__Make sure the version is incremented__ in `./setup.py`

### Install via `.whl` (wheel)

Generate `.whl`

```bash
source env/bin/activate # if not already
python setup.py bdist_wheel -d dist
```

Install .whl

```bash
# this creates an wheel archive which can be copied to a deployment location, e.g.
scp dist/analyse_ta.X.X.X-py3-none-any.whl user@host:~/wheels
# on host
pip install --find-links=~/wheels analyse_ta
```

### Reference
<!--refs-->
 [Nature]:https://www.nature.com/articles/s41586-020-2769-8
 [samtools]: http://www.htslib.org
 [analyse_ta-releases]: https://github.com/cancerit/ta_analyser/releases

