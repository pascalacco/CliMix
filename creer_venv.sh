#!/bin/bash
rm -rf venv &&
<<<<<<< HEAD
    python3 -m venv venv &&
    . venv/bin/activate &&
    python3 -m pip install --upgrade pip &&
=======
    python -m venv venv &&
    . venv/bin/activate &&
    python -m pip install --upgrade pip &&
>>>>>>> 84fc7ab9326e42e4812f6ac8c566599650b9eaaf
    pip install -r requirements.txt &&
    pip install -e .
