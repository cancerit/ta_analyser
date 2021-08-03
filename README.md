# analyse_ta
| Master                                              | Develop                                               |
| --------------------------------------------------- | ----------------------------------------------------- |
| [![Master Badge][travis-master-badge]][travis-repo] | [![Develop Badge][travis-develop-badge]][travis-repo] |

This project hosts scripts to analyse TA repeats coverage calculated using samtools bedcov command 

`samtools bedcov data/

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
 [samtools]: http://www.htslib.org
 [travis-master-badge]: https://travis-ci.org/cancerit/annotateVCF.svg?branch=master
 [travis-develop-badge]: https://travis-ci.org/cancerit/annotateVCF.svg?branch=develop
 [travis-repo]: https://travis-ci.org/cancerit/annotateVCF
 [analyse_ta-releases]: https://github.com/cancerit/annotateVCF/releases
