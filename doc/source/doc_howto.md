
# Générer cette doc


On utilise *Sphynx* pour générer les pages html dans `doc/build/html` à partir du code python dans `flaskapp/` et de sources écrites manuellement en markdown dans `doc/source`

Pour cela il faut :

  1. Lancer la [commande make](#1---commande-make)
  2. Puis [visualiser la doc](#2---visualiser-la-doc)
  3. Pour modifier la doc voir le schéma de la [structure de la doc](#structure-de-la-doc-sphynx)

## 1 - Commande make

Dans un terminal se placer dans le répertoire du dépot git `CliMix` :
 1. Bien s'assurer que les paquets python sont installés
    * Si dans un environnement virtuel faire   
        ```bash 
        source venv/bin/activate
        ```   
        Sinon rien
    * Installer les requirements   
        ```bash 
        pip install -r requirements
        ```   
 2. Lancer la commande make
    ```bash
    cd doc  
    make html
    ```   

## 2 - Visualiser la doc
Naviguer et ouvrir le fichier `doc/build/html/index.html`   
ou bien sous linux   
```bash
firefox ./doc/build/html/index.html
```   


## Structure de la doc sphynx

Les fichier éditables sont les `.md` de `doc/source/` et le `doc/source/index.rst`   
Les commentaires du code `.py` du répertoire `flaskapp/` sont autogénérés 

```mermaid
%% Syntaxe ici https://mermaid.js.org/intro/syntax-reference.html
    graph TD;
    subgraph "flaskapp/"
        py1["flaskapp/*.py"]
        py2["..."]
        py3["flaskapp/*.py"]
    end
    subgraph "doc/source/"
        subgraph "génération automatique"
            rst1["doc/source/*.rst"]
            rst2["..."]
            rst3["doc/source/*.rst"]
            py1 -- autogen --> rst1
            py2 -- autogen--> rst2
            py3 -- autogen--> rst3
            modules["doc/source/modules.rst"]
        end

        subgraph "édition  manuelle"
            md1(doc/source/*.md)
            md2(...)
            md3(doc/source/*.md)
            indexrst[doc/source/index.rst]
        end
    end
    subgraph "doc/build/html/"     
        rsthtml1["<*rst>.html"]
        rsthtml2["..."]
        rsthtml3["<*rst>.html"]
        rst1 -- render --> rsthtml1
        rst2 -- render --> rsthtml2
        rst3 -- render --> rsthtml3
        mdhtml1["<*md>.html"]
        mdhtml2["..."]
        mdhtml3["<*md>.html"]
        md1 -- render --> mdhtml1
        md2 -- render --> mdhtml2
        md3 -- render --> mdhtml3
        indexhtml["index.html"]
        indexrst -- render --> indexhtml
        moduleshtml["modules.html"]
        modules -- render --> moduleshtml
        %%md1 & md2 & md3 -- include --> indexrst
        %%modules -- include --> indexrst
        %%rst1 & rst2 & rst3 -- include --> modules
        mdhtml1 & mdhtml2 & mdhtml3 -. inclusion .-> indexhtml
        rsthtml1 & rsthtml2 & rsthtml3 -. inclusion .-> moduleshtml
        moduleshtml -. inclusion .-> indexhtml
 end 
```



