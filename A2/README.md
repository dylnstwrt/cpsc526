# Assignment 2, Question 1 - CPSC 526
Name: Dylan Stewart, UCID :30024193

## Installation

In directory ```A2```, run either:
```
make init
```
or
```
pip3 install -r requirements.txt
```

## Usage

In the directory ```A2/a2```, to execute enroll.py, authenticate.py, or tests.py, please use ```python3```. If running ```tests.py```, feel free to use the ```-v``` flag to see the status of each test.

## Notes

The following uses the library [argon2-cffi](https://argon2-cffi.readthedocs.io/en/stable/) which implements the argon2 hashing algorithm in python. The hashes that are produced using this library are encoded in a format specific to the library, which includes a randomly generated salt with it.

## License
[MIT](https://choosealicense.com/licenses/mit/)