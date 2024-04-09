.ONESHELL:

venv :
	./creer_venv.sh
	touch venv/touche

maj_python : venv/touche venv/climix_touche

venv/touche : requirements.txt notebooks_requirements.txt
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	. venv/bin/activate && pip install -r notebooks_requirements.txt
	touch venv/touche

venv/climix_touche : setup.py $(wildcard  climix/*.py) $(wildcard climix/*/*.py) $(wildcard flaskapp/*.py) $(wildcard pythonapp/*.py) 

	. venv/bin/activate && pip install -e .
	touch venv/climix_touche

exec_locale : 
	. venv/bin/activate && python flaskapp/app.py

edit :
	source venv/bin/activate
	pycharm.sh .

doc :
	. venv/bin/activate && make -C doc html

deploiement_test :
	. ./deploiement.sh && redeplois . /var/www/climix-test

deploiement_stable :
	. ./deploiement.sh && redeplois . /var/www/climix

.PHONY : venv deploiement_test deploiement_stable  exec_locale doc
