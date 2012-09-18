from Mojo.Forms.MojoFormHelper import Form, model_as_form
from models import BlogPost

thisForm = model_as_form(BlogPost, ignore=['tags', 'comments'])

for f in thisForm._fields:
    print "Name: %s Type: %s" % (f, str(type(thisForm._fields[f])))

