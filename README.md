# CliMix

Pour générer la doc dans votre répertoire git allez voir les [instructions sur le Github](https://github.com/pascalacco/CliMix/blob/doc/doc/source/doc_howto.md)



## Machine à état des pages

```mermaid
%% Syntaxe ici https://mermaid.js.org/intro/syntax-reference.html
%% Un diagrame de séquence serait plus approprié
  graph TD;
  subgraph "client html"
     index["index.html"] 
     photo["photo.html"]
     manual["manual.html"]
     
     cookie[("cookie \nGroupe+Equipe")]     
     cookphoto{ }
     photo -- noPhotoBtn --> rendermanual


  end
  subgraph "serveur flask"

     save{save.json}
     mix{mix.json}
     
     results{results.json}
     root["/"]
     setgroup([/set_group])
     ajaxphoto["/photo"]
     rendermanual["/manual"]

     root -- "render" --> index
     index -- logInButton --> setgroup
     setgroup -.- init -.-> cookie & save & mix & results 
     setgroup -- successs --> rendermanual

     ajaxphoto -- cookie présent --> cookphoto --> photo
     ajaxphoto -- cookie absent --> root
     cookie -.-> cookphoto
     rendermanual -- render --> manual
  end
```
## Installation

### Prérequis
python3.6 ou supérieur

### Installation des dépendances
```bash
pip install -r requirements.txt
```
### personnalisation des chemins
Dans le ficher flaskapp/constantes.py, modifier les chemins
 

