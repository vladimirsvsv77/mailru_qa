from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.mairudata
questions = db.mairudata

print(len(list(questions.find())))

q = list(questions.find())
print(q[len(q) - 1])