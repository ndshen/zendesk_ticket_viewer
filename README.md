# Zendesk Ticket Viewer

This is a coding challenge for Zendesk 2022 Summer Internship by _\_PingYao Shen_.  
See [demo](https://terminalizer.com/view/160a8e4f5403).

## Prerequisite

This is a Python project. Please make sure you have [Python installed](https://www.python.org/downloads/) on your machine. **The minimum version of Python is 3.9.0**, however, I developed with Python 3.10.0, therefore **Python 3.10.0 is strongly recommended**.

#### Install Python 3.10.0

If you currently don't have Python 3.10.0 but have other versions installed. I recommend using [Pyenv](https://github.com/pyenv/pyenv#installation). Pyenv helps you manage all the different Python versions installed on your machine. To learn more about Pyenv and how to install it on different operating sytems, here's an amazing [article](https://realpython.com/intro-to-pyenv/).

#### Install Dependencies

[Pipenv](https://github.com/pypa/pipenv) is another amazing tool that manages virualenv for python projects. Once you have pipenv installed (and Python 3.10.0 installed too), run this command to create a virtual environment for this project, and install all the required dependencies in it:

```shell
cd /path/to/this/project/zendesk
pipenv install
```

In the **Pipfile**, you can see that the required python version is 3.10.0, therefore, `pipenv install` will only work if you have python 3.10.0. If you only have python 3.9+ or you don't want to install Pipenv, you can also use the traditional way:

```shell
pip install -r requirements.txt
```

## Usage

Run one of these commands to start the program:

```shell
# if you installed the dependencies with pipenv
pipenv run python ./zendesk_ticket_viewer/main.py

# if you installed the dependencies with requirements.txt
python ./zendesk_ticket_viewer/main.py
```

Run the tests:

```shell
# if you installed the dependencies with pipenv
pipenv run python -m unittest

# if you installed the dependencies with requirements.txt
python -m unittest
```
