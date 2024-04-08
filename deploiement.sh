TMP="/tmp"

sauve(){
    cp -rf "$1"/flaskapp/game_data "$2"/flaskapp/game_data
    rm -f "$2"/flaskapp/game_data/*.*
    cp -rf "$1"/venv "$2"/venv
}


copy(){
    cp -r "$1"/flaskapp "$2"/flaskapp
    cp -r "$1"/*.sh "$2"/
    
  rm -rf "$2"/.git
}


synchronise()
{
    rm -rf "$1/tmp" &&
	mkdir "$1/tmp" &&
	mkdir "$1/tmp/flaskapp" &&
	sauve "$2" "$1/tmp" &&
	rm -rf "$2/*"&&
	copy "$1" "$2" &&
	sauve "$1/tmp" "$2" &&
	rm -rf "$1/tmp" "$2/tmp"
}

rsynchronise(){
    rsync -av --delete --exclude={'.git','flaskapp/game_data/*/*','venv','doc/build'} --include={'flaskapp/game_data/*.json'} "$1/" $(realpath -s "$2")
}


redeplois(){
    echo "Synchronise $1 et $2"
    synchronise $1 $2

    echo "Mise à jour du venv"
    cd "$2" && make maj_python

    echo "Droits de modifs pour $PWD/flaskapp/game_data"
    chmod -R a+rw flaskapp/game_data/*/*

    echo "compilation de la doc"
    make doc
    
}


reinit(){
    rm -rf $2/*
    mkdir $2
    copy $1 $2
    cd "$2"
    echo 'dataPath="'"$2"'/flaskapp/"' > flaskapp/constantes.py
    chmod -R a+rw flaskapp/game_data/*/*
    make venv && source venv/bin/activate && make doc
}
