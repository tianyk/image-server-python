from bson import objectid

id = objectid.ObjectId()
print id
print id.generation_time
print type(id.generation_time)
print type(id)
print str(id)