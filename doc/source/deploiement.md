# Déploiement sur le site web
La branche `master` est tirée sur le serveur pour mettre à jour le soft.

## Modifications git

En général :
 1. on travaille sur une branche de developpement (par exemple ̀`dev`)
 2. on teste en local si les modifications sont bonnes
 3. on merge la branche `dev` dans le master
 4. on télécharge la branche sur le serveur

### 1 - Modif d'une branche

La première fois on créés  une branche de travail  
  ```bash 
  git checkout master
  git checkout -b <ma branche par exemple "dev">
  ```
Les autres fois on reste ou se met sur la branche dev et on regarde s'il y a du nouveau venant des autres...
  ```bash 
  git status
  git checkout dev
  git pull
  ```
 Si pb et que l'on veux abandonner SA version et prendre celle des autres (perdre ses modifs) 
```bash
git reset --hard
```

 On travailles sur sa branche et lorsque l'on a fini une étape, on ajoute les modifs et fait un commit(local) et on fait un push (sur le serveur Git) :
```bash
git add .
git commit -m"message genre fini la doc de truc"
git push
```

### 3 - merge sur la branche master

Lorsque tout est bon et que l'on veut publier, on va sur la branche master, on merge la branche dev, et on push sur le serveur Git :
```bash
git chekout master
git merge dev
git push
```

## 4 - télécharge sur le serveur WEB
On fait une connexion distante `ssh` sur le serveur et on tire la branche master

1. Se connecter à l'INSA avec le VPN
2. On lance la commande pull sur le serveur via ssh :

    ```bash
    ssh user@srv-geitp -p2222 "cd /var/www/html; git pull"
    ```
    Le mot de passe est "egats" en verland.

    
## 5 - Modif de appache sur apps-geitp
 0. se connecter `ssh user@srv-geitp -p2222`
 1. modifier `/etc/apache2/sites-available/000-default.conf`
 2. relancer appache  `sudo systemctl restart apache2`
 3. vérifier que c'est repartis `sudo systemctl status apache2`