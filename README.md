# fastapi-example
Example project with a few simple APIs that don't do much and pytests to check them.


# Requirements
Python (tested on python 3.11.3)
Docker


# How to run:

clone it  
cd into it  
make build  
make run  
open browser http://localhost:3000/

# How to work with requirements file
The recommendation is to use pipdeptree to create the requirement files.  
Simply run `make freeze` to get a requirement file in a tree format.
That way it will be clear what are the top level requirements.
