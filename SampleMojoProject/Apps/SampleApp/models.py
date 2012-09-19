from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import *
import datetime

class Tag(Model):
    tag_name = StringField()


class Comment(Model):
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
    tags = ListField(of=Tag)
    comments = ListField(of=Comment)
    published = BooleanField(default=True)