#!/bin/bash

export PYTHONPATH=$(pwd)/src

python3 -m unittest discover -s src/test