#!/bin/bash
rm -rf venv &&
    python -m venv venv &&
    . venv/bin/activate &&
    python -m pip install --upgrade pip &&
    pip install -r requirements.txt &&
    pip install -r notebooks_requirements.txt &&
    
    pip install -e .
