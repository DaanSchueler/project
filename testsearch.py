import requests
import json
import pprint as pp

t = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e")
x = json.loads(t.text)
print(x)
for i in x['matches']:
    print ( i['imageUrlsBySize']['90'])

for i in x['matches']:
    print (i['recipeName'])

# Easy Healthy Maple Glazed Salmon in Foil
# https://lh3.googleusercontent.com/Of0nipZXlHplyCI1Fw--rGNe7Rcj5HXAyI-cWjmqJBtYg0BRF6E43Y7RxA690eUdQykHZP8twgfjn64HN7Fa2A=s90-c




#     0
# imageUrlsBySize
# 90


# &allowedAllergy[]=393^Gluten-Free

