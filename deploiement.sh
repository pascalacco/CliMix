copy(){
    rm -rf "$2"/game_back
    mv -f "$2"/flaskapp/game_data "$2"/game_back
    rm -f "$2"/game_back/*.*
    rm -rf "$2"/flaskapp
    rm -f "$1"/flaskapp/app.wsgi
    cp "$1"/flaskapp/app-test-sample.wsgi  "$1"/flaskapp/app.wsgi
    rm -rf "$1"/flaskapp/game_data/*/*
    cp -rf "$1"/flaskapp "$2"/flaskapp
    cp -rf "$1"/*.sh "$2"/
    cp -rf "$1"/*.txt "$2"/
    cp -rf "$1"/Makefile "$2"/
    cp -rf "$1"/setup.py "$2"/
    cp -rf "$1"/doc "$2"/
    
}


synchronise()
{
    
    copy "$1" "$2"
}

rsynchronise(){
    rsync -av --delete --exclude={'.git','flaskapp/game_data/*/*','venv','doc/build'} --include={'flaskapp/game_data/*.json'} "$1/" "$2/"
}



redeplois(){
    SRC=$(realpath -s "$1")
    DST=$(realpath -s "$2")
    
    echo "__________________________________________________"
    echo "Synchronise $SRC et $DST"
    echo "__________________________________________________"
    rsynchronise "$SRC" "$DST"

    echo "__________________________________________________"
    echo "Mise à jour du venv"
    echo "__________________________________________________"
    cd "$DST" && make maj_python

    
    echo "__________________________________________________"
    echo "Droits de modifs pour $PWD/flaskapp/game_data"
    echo "__________________________________________________"
    cd "$DST" && mkdir -p ./flaskapp/game_data &&
	chmod -R a+rw flaskapp/game_data

    echo "__________________________________________________"
    echo "compilation de la doc"
    echo "__________________________________________________"

    cd "$DST" && make doc
    echo "__________________________________________________"

    pwd
    cd "$SRC"
    pwd

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
