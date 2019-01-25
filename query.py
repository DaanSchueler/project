import requests
import json
import pprint as pp
from cs50 import SQL

db = SQL("sqlite:///recepts.db")
fired_button =  requests.post['data']
print(fired_button)
s = requests.get("http://api.yummly.com/v1/api/recipe/{}?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e".format(fired_button))
y = json.loads(s.text)
recipe_image = y['images'][0]['imageUrlsBySize']['360']
recipe_name = y['name']
result = db.execute("INSERT INTO likes (username, recipe_id, recipe_name, recipe_image) VALUES(:username, :id, :name, :image)",
                        username= "ruben", id = fired_button, name = recipe_name, image = recipe_image)
