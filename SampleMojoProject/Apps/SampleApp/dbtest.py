from models import *

value_list=[1,2,3]
v2 = []
for item in value_list:
    t = Tag()
    t.tag_name = item
    v2.append(t)


for p in v2:
    print 'DOT: ', p.tag_name
    print 'DICT: ', p['tag_name']
    p.save()


#class mDict(dict):
#    def __init__(self):
#        class_attrs = [attr for attr in self.__class__.__dict__ if '__' not in attr]
#        for c in class_attrs:
#            self[c] = self.__class__.__dict__[c]
#
#    def __getattr__(self, item):
#        if self.has_key(item):
#            return self[key]
#        else:
#            return None
#
#    def __setattr__(self, key, value):
#        self[key] = value
#
#
#class ndict(mDict):
#    banana = 'banana'
#
#c = []
#for a in xrange(3):
#    b = ndict()
#    b.banana = a
#    c.append(b)
#
#print c

