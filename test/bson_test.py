from bson import objectid

id = objectid.ObjectId()
print id
print id.generation_time
print type(id.generation_time)
print type(id)
print str(id)

print id.generation_time.strftime("%Y%m%d")
print objectid.ObjectId.is_valid("dfefefwef")
print objectid.ObjectId.is_valid(id)