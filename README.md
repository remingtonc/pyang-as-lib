# pyang-as-lib
Use [pyang](https://github.com/mbj4668/pyang) as a library for custom parsing of attributes from YANG models.

## Installation

```bash
cd pyang-as-lib
pip install --upgrade --user pipenv
pipenv --three install
```

## Usage

```bash
pipenv shell
python parse_model.py
# Outputs to testout.json
more testout.json
exit
```
