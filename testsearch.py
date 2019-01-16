import requests
import json
import pprint as pp

t = requests.get("http://api.yummly.com/v1/api/recipes?_app_id=6553a906&_app_key=21ef3e857585ece9f97b0831c08af72e&allowedAllergy[]=393^Gluten-Free")
x = json.loads(t.text)

# for i in range(len(x["matches"])):
#     pp.pprint(x["matches"][i])
#     print()

print(x)