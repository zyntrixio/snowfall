# SnowFall

## Description

[Provide a brief description of your project here.]

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

Firstly, ensure that Python 3.12 and Poetry are installed on your system:

```shell
$ brew install python@3.12 poetry
```

Clone the repository:

```shell
$ git clone git@github.com:binkhq/SnowFall.git
```

Set the `keyvault_url` with the desired Snowflake credenitals in your `.env` file, example:
```
KEYVAULT_URL=TBD
```

Setup a virtual environment via Poetry to begin development.
```shell
$ poetry install
$ poetry shell
```

## Usage

To serve the code locally, use the below.

```shell
$ tbd
```


## Testing

To test the repository, we are using `pytest` and `dash.testing`

Pytest will be used to test python functions as part of our unit testing approach.

Testing can be run via the below command:

```Shell
$ pytest
```

## Contributing

Please ensure that you follow the below steps to contribute to this repository.

If you have installed new dependancies to the venv, then run the below command:

```shell
$ poetry add {pagckage name} # to add new package
```

This will allow other developers to install these dependancies on their system as well as update production.

Next, when creating a new `.py` file or fixing an existing file, please create a branch, and open a pull request to add this to the master branch.

Ensure all code is documented and tested as per the above testing documentation, and new unit tests are implemented for new functions.
