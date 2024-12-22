import logging

from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases

client = Client()
database_id = "670f873d003d1701a4b4"
collection_id = "6767e40c000dbb7cbc96"

client.set_endpoint('https://cloud.appwrite.io/v1')  # URL de votre instance Appwrite
client.set_project('670aa8db002c0cbb4178')  # Votre ID de projet
client.set_key(
    "standard_0d087d2c172f371b8d0efc8f22902765e8936a30803a4e2b99f9cdefaee1f563b2b246036451bd6639a40f8b2eb4397bb99b1662368a5582a2a1a975d2b4f43e3fd4079d293bb51102cea470ffc6e6195c8e5e8cc7be3ea921924b214c982615c8a5723b3960a4192af6b07db1375810ba2946f249b08e60e2bb393d3b4e8ac7")

account = Account(client)
database = Databases(client)


# default password
# password = "123456789"

def create_client_user(matricule, nom):
    try:
        password = f"{matricule + nom[:5]}"
        logging.warning(f"Création de l'utilisateur {matricule} au mot de passe {password}")
        new_account = account.create('unique()', f"{matricule}@enspd.com", password)
        logging.warning(f"Création de l auth {new_account} réussie")
        if not new_account:
            raise ValueError("Erreur lors de la création de l'utilisateur")
        new_user = database.create_document(database_id, collection_id, 'unique()',{
            'accountId': new_account.get('$id'),
            'username': nom,
            'matricule': matricule,
        })
        logging.warning(f"Création de l'utilisateur {new_user} réussie")
        return new_user
    except Exception as e:
        logging.error(f"Erreur lors de la création de l'utilisateur {matricule}")
        logging.error(e)
        raise ValueError("Erreur lors de la création de l'utilisateur")
