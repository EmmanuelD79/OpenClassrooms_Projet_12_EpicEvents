# **P12 EPIC EVENTS**

Projet "Développez une architecture back-end sécurisée en utilisant Django ORM" d' OPENCLASSROOMS - formation développeur Python.

### **Le contexte du projet**:
EPIC EVENTS organise pour ces clients des fêtes et des événements hors du commun. 
Le fournisseur du CRM de l'entreprise a été piraté et des informations relatifs aux clients de l'entreprise ont été compromise.
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

8. La mise en place de filtre et recherche sur les Endpoints de l'API et dans l'interface web.


## **Documentation**:

La documentation de l'API est accessible à l'adresse : https://documenter.getpostman.com/view/23145404/2s847HNXSB

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

Pour des raisons de sécurité, un fichier de configuration `init_config.py` est nécessaire à la configuration du projet.

Veuillez à créer un fichier `ìnit_config.py` à la racine du projet avec les constantes suivantes :

```python

SENTRY_DNS = "https://<key>@sentry.io/<project>"
SECRET_KEY = 'yout_secret_key_django'
DB_USER = 'your_user_db'
DB_NAME = 'your_db_name'
DB_PASSWORD = 'your_db_password'
DB_HOST = 'your_db_host'
DB_PORT = 'your_db_port'
DB_TEST = {
    'NAME': 'your_db_test_name',
        }
ADMIN_ID = 'your_admin@email.com'
ADMIN_PASSWORD = 'your_admin_password'
ADMIN_FIRST_NAME = 'your_admin_first_name'
ADMIN_LAST_NAME = 'your_admin_last_name'

```

## **Monitoring du Projet avec SENTRY**

Le monitoring du projet est prévu avec sentry.io.

Si vous voulez l'utiliser,

Au préalable:

* Vous devez créer un compte sur le site sentry.io et suivre les instructions pour obtenir votre "Key".
* Saisir le dns avec la "Key" dans le fichier de `init_config.py` dans la constante `SENTRY_DNS`


Ensuite, décommenter les lignes suivantes dans le fichier `settings.py`:

```
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://<key>@sentry.io/<project>",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

```

Pour tester votre configuration, vous pouvez décommenter les lignes suivantes dans le fichier `urls.py` du dossier EpicEvents:
```
from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0
```

et
```
path('sentry-debug/', trigger_error),
```
dans `urlpatterns`.

L'accèsl à l'url `sentry-debug/' provoquera une erreur et elle sera relevée par sentry.


## **Démarrage**

Pour démarrer le projet, vous devez aller dans le répertoire du projet et taper sur votre terminal les commandes:

```

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

La création de l'administrateur et des groupes d'utilisateur nécessaire au fonctionnement du projet peuvent être créer grâce à la commande :

```
python manage.py init_project

```

Il est possible d'injecter des données de démonstration dans la base de données avec la commande :

```
python manage.py init_local_db

```

L'application web est disponible en local à l'adresse:  http://localhost:8000/crm/

Pour utiliser l'API:
```
http://localhost:8000/api/

```
puis vous connecter et récupérer les tokens sur l'endpoint :
```
http://localhost:8000/api/login/

```
