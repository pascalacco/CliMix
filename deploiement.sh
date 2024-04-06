python -m pip install --upgrade pip 
pip install -r requirements.txt 
pip install -r notebooks_requirements.txt
pip install -e .
chmod -R a+rw flaskapp/game_data/*/*
make doc
