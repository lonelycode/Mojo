from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import StringField, ObjectIDField
from pymongo_backend import Session, Collection

class messages(Model):
    _id = ObjectIDField()
    msg = StringField()


s = Session(db_name='test')
c = Collection(s, messages)

m = messages()
m.msg = u"New message!!!"

docs = c.insert([m])
for a in docs:
    print 'Doc', a

single_doc = docs[0]

print 'Single doc: ', single_doc

from bson.objectid import ObjectId
print 'finding: ', type(single_doc._id.get_value())
#ObjectId('504875716b7e15388f088a7c')}
obj = c.find_one({"_id":single_doc._id.get_value()})

print "Returned: ", obj

print 'Modifying and saving:'
obj.msg = u"I've changed!"
print c.save(obj)

print 'Finding many'
items = c.find({})

print items

print 'deleting'
print c.delete([obj])