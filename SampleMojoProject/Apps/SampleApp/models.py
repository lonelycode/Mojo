from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import *
import datetime

class Tag(Model):
    _id = ObjectIDField()
    tag_name = StringField()


class Comment(Model):
    _id = ObjectIDField()
    handle = StringField()
    comment = StringField()
    visible = BooleanField(default=True)


class BlogPost(Model):
    _id = ObjectIDField()
    title = StringField(allow_empty=False)
    slug = StringField(allow_empty=False)
    post_intro = StringField()
    post_body = StringField()
    date_published = DateTimeField(default=datetime.datetime.now())
    tags = ListField()
    comments = ListField()
    published = BooleanField(default=True)