import pprint
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}

db = {}
db['bob'] = bob
db['sue'] = sue

for record in db.values(): print(record['pay'])