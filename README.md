# **P12 EPIC EVENTS**

Projet "Développez une architecture back-end sécurisée en utilisant Django ORM" d' OPENCLASSROOMS - formation développeur Python.

### **Le contexte du projet**:
EPIC EVENTS organise pour ces clients des fêtes et des événements hors du commun. 
Le fournisseur du CRM de l'entreprise a été piraté et des informations relatifs aux clients de l'entreprise ont été comprimose.
L'entreprise a décidé de développer en interne un CRM avec Django.

### **Le projet**:
Créer un CRM avec une interface web et une API:

1. L'authentification des utilisateurs.

2. Les opérations CRUD sur les employés, les clients, les contrats et les évenements.

3. La gestion des permissions et autorisations de l'utilisateur connecté sur les vues et opérations.

4. Personalisation du système d'administration de Django.

5. Définir des endpoints et fournir une documentation pour l'API.

6. La sécurisation des accès et données suivant l'OWASP.

7. L'utilisation d'une base de données PostgreSQL.


## **Documentation**:

La documentation de l'API est accessible à l'adresse : 

Vous y trouverez la définition de chaque endpoint avec les données à fournir et les réponses attendues.

<br>

## **Pré-requis**

Vous pouvez accéder au projet en :

* clonant le projet à l'aide de votre terminal en tapant la commande :
<br> 

```

    https://github.com/EmmanuelD79/OpenClassrooms_Projet_12_EpicEvents.git


```

* créer un environnement virtuel à l'aide de votre terminal en tapant la commande:

```

    python -m venv env

```

* puis l'activer :
  * sur windows :

    ```

        .\env\scripts\activate

    ```

  * sur mac et linux :

    ```

        source env/bin/activate

    ```

<br>

## **Installation**

Pour utiliser ce projet, il est nécessaire d'installer les modules du fichier requirements.txt.

Pour installer automatiquement ces modules, dans votre terminal, vous devez aller dans le dossier du projet et ensuite taper la commande suivante :
```

pip install -r requirements.txt

```

ou le faire manuellement en consultant le fichier requirements.txt en tapant sur votre terminal la commande :

```

cat requirements.txt

```

puis les installer un par un avec la commande :

```

pip install <nom du paquage>

```
<br>

## **Démarrage**

Pour démarrer le projet, vous devez aller dans le répertoire du projet et taper sur votre terminal la commande:

```

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```


L'application web est disponible en local à l'adresse:  http://localhost:8000/

Pour utiliser l'API:
```
http://localhost:8000/api/

```
puis vous connecter et récupérer les tokens sur l'endpoint :
```
http://localhost:8000/api/login/

```