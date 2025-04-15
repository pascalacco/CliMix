SHELL := /bin/bash
.ONESHELL:

venv :
	./creer_venv.sh
	touch venv/touche

maj_python : venv/touche venv/climix_touche

venv/touche : requirements.txt notebooks_requirements.txt
	source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	source venv/bin/activate && pip install -r notebooks_requirements.txt
	touch venv/touche

venv/climix_touche : setup.py $(wildcard  climix/*.py) $(wildcard climix/*/*.py) $(wildcard flaskapp/*.py) $(wildcard pythonapp/*.py) 

	source venv/bin/activate && pip install -e .
	touch venv/climix_touche

exec_locale : 
	source venv/bin/activate && python flaskapp/app.py

edit :
	source venv/bin/activate
	pycharm.sh .

doc :
	source venv/bin/activate &&  cd ./doc && ./apidoc_modules.sh && make  html

deploiement_test :
	source ./deploiement.sh && redeplois . /var/www/climix-test

deploiement_stable :
	source ./deploiement.sh && redeplois . /var/www/climix

deploiement_public :
	source ./deploiement.sh && redeplois . /var/www/climix-public



venv_reset :
	rm -rf venv
	mdir venv
	./creer_venv.sh

.PHONY : venv deploiement_test deploiement_stable  exec_locale doc
