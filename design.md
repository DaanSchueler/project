#Controllers

##Homepage
Get:
Ophalen top recepten om deze op de homepage te plaatsen, clickable.
(Mogelijk zichtbare counter bij recepten)
Render homepage

POST: Mogelijk klikken op favoriet bij elke recept (toevoegen/verwijderen). -> (Misschien java?)  of Redirect naar persoonlijke pagina.  = Toevoegen/ verwijderen aan/van persoonlijk favorieten + favoriet counter ++  (Insert in database)

##Register
Get:
Session clear, Render register

Post:
Registreer gebruiker, Insert in database gebruiker en password ,(email), ophalen id,  maak sessie,  redirect hompage (logged in)

##Log in / Log out
Get :
Session clear, render log in

Post:
Find/ check user details,  ophalen id,  create session

##Persoonlijke pagina (public)
Get:
Ophalen favorieten van user, gesorteerd op recent
Render persoonlijke pagina

Post:
Verwijder favoriet, verwijderen uit database -> blijf op zelfde pagina (Java?) -> render persoonlijke pagina

##Search
Get:
Render search template

Post:
Search button, alle filters die worden ingevuld: (Allergie, dieet, include, exclude)
Recepten ophalen uit database gebaseerd op filters (gesorteerd op? )

##Results
Get: render results (Met alle benodigde variabelen en filters.
Sorteer functies (tijd, alfabetisch etc)

Post: Favoriete toevoegen/ verwijderen binnen de resultaten, toevoegen/verwijderen uit database

#Views
schetsen

#Models/helpers (Grote functies / functies die we vaak nodig hebben)
Variant op apology: Om an te geven dat er een error plaats heeft gevonden

Toevoegen/ verwijderen favoriet: Het toevoegen of verwijderen van een recept uit de favorieten van een gebruiker

Zoekmachine: Het ophalen van de zoekresultaten en het reformateren van de data

#Plugins en frameworks
Flask
Bootstrap
Javascript
AJAX
PHP
Java