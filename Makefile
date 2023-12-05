.ONESHELL:

venv :
	./creer_venv.sh


deploiement : 
	cp -rf flaskapp /var/www/html/flaskapp
	chmod a+w -R /var/www/html/flaskapp/game_data

exec_locale : 
	. venv/bin/activate && python flaskapp/app.py

deploiement_doc :
	cp -rf doc/build/html /var/www/html/doc

maj_python : venv/touche venv/climix_touche

venv/touche : requirements.txt
	venv/bin/pip install -r requirements.txt
	touch venv/touche

venv/climix_touche : setup.py foret/*.py
	venv/bin/pip install -e .
	touch venv/climix_touche

.PHONY : venv deploiement exec_locale 
