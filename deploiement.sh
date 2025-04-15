
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
    cd "$DST" && pwd &&make maj_python

    
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
