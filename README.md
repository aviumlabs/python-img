# Avium Labs Python Docker Image

This is a Python Docker image based on the Python Alpine Linux docker image.
GitHub URL: https://github.com/aviumlabs/python-img

## Recent Updates
**2026-11-16**
* Updated stack:
  * Python 3.15.2

## Build an Image

### Default Image Build

If using the default image the APP_NAME is `app`. 

**Regular build**  
```shell
docker build --pull --no-cache -t aviumlabs/python:3.15-lab-alpine .
```

**Build with sbom and provenance** 
```shell
docker build --pull --no-cache -t aviumlabs/python:3.15-lab-alpine --provenance=mode=max --sbom=true .
```

### Building an Image with a Specific App Name 

```shell
export APP_NAME=myapp
```

**Regular build**  
```shell
docker build --pull --no-cache -t aviumlabs/python:3.15-lab-alpine --build-arg APP_NAME=$APP_NAME .
```

**Build with sbom and provenance** 
```shell
docker build --pull --no-cache -t aviumlabs/python:3.15-lab-alpine --build-arg APP_NAME=$APP_NAME --provenance=mode=max --sbom=true .
```

## Run

Running the default image:  

```shell
export APP_NAME=app
```

```shell
docker run --name $APP_NAME -p 8888:8888 -it -e APP_NAME=$APP_NAME --rm -w "/opt/python/$APP_NAME" --mount type=bind,src="$(pwd)/src",target="/opt/python/$APP_NAME" --mount type=bind,src="$(pwd)/tests",target="/opt/python/tests" --mount type=bind,src="$(pwd)/dist",target="/opt/python/dist" aviumlabs/python:3.15-lab-alpine
```
During the container startup, the login URL will be printed out:

>  
> http://127.0.0.1:8888/lab?token=<string>
>  

Copy this URL to access the Juptyer Lab environment in a browser.

## JupyterLab

After opening JuptyerLab in a broswer, you'll see the landing page. 

To start a new Notebook:
- Select Launcher > Notebook > Python 3

When you save a Notebook, it is saved to the src directory be default, which is a bind
mounted diretory on your local hard drive.

## Archive

### Design 

The src directory is bind mounted into the Docker container and the 
container provides the Python runtime environment.   

There are two supporting scripts that provide `aliases` for running python 
commands in the docker container:  
* .appdev - supports macOS and Linux  
* .appdev.ps1 - supports Windows  

The three aliases are:  
* pip  
* python  
* pytest  

If you need to run `pip`, `python`, or `pytest` in the container, source the 
alias file prior to running the command:    

```shell
. ./.appdev
```

```PowerShell
. .\.appdev.ps1
```


The included `requirements.txt` file installs the following python packages 
and their dependencies:

* build
* hatchling
* loguru
* pytest
* python-dateuitl
* jupyterlab
* pydantic
* langchain


This file may be deleted and recreated with project specific requirements.  

There are two methods for adding additional packages.

1. Directly editing requirements.txt.
2. Running pip install.

**To install Python packages with pip:**
* Source the included .appdev file in a shell session
* Run pip install <package>
* Run pip freeze to export application requirements
* Continue with coding

```shell
. ./.appdev
```
```shell
pip install <package>
```
```shell
pip freeze > requirements.txt
```

The appdev PowerShell script has not been tested. Please file an 
issue if it does not work.

```PowerShell
. .\.appdev.ps1
```
```PowerShell
pip install <package>
```
```PowerShell
pip freeze > requirements.txt
```

### Development Environment

This is carry over from the base image and would not be used in this environment.

Modify the pyproject.toml file to meet your requirements. 

**Recommendation is to not use spaces or special characters in the name and keep it short.**


#### Coding

All of the code for the application is in the `src/` directory and it is 
stored on your computer's local filesystem and not in the docker container.

Use your favorite editor to write your application code.


#### Build a Package

The environment has built in support for building a package. The `dist` 
directory is bind mounted into the container, and running `build` will 
create a python package in the `dist` directory on your local filesystem. 

```shell
. ./.appdev
```
```shell
python -m build
```

#### Pytest Integrated

The environment has integrated support for `pytest`. Create your **test** 
files in the `tests` directory and run pytest in the docker container.

```shell
. ./.appdev
```

Run standard pytest:  
```shell
pytest 
```

Run pytest and print output:  
```shell
pytest -s
```

To run specific test file with output:  
```shell
pytest -s tests/test_<file_name>.py
```   

## Interal

### Push Docker Image

```shell
docker push aviumlabs/python:3.15-lab-alpine
```