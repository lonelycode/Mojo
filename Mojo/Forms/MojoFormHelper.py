# -*- coding: utf-8 -*-
# This is modified from Lepture's gist: https://github.com/lepture/tornado.ext/blob/master/forms.py

import re
import tornado.locale
from tornado.escape import to_unicode
from wtforms import Form as wtForm

class Form(wtForm):
    """
    A wrapper around the standard ``wtForms`` ``Form`` object that integrates with tornado. Modified slightly for compatibility
    with Mojo models - you can pre-populate a form and populate a model using this Form class instead of the standard
    wtForms Form.

    Example::

        class SigninForm(Form):
            email = EmailField('email')
            password = PasswordField('password')

        class SigninHandler(RequestHandler):
            def get(self):
                form = SigninForm(self.request.arguments, locale_code=self.locale.code)

    """
    def __init__(self, formdata=None, obj=None, prefix='', locale_code='en_US', **kwargs):
        self._locale_code = locale_code
        super(Form, self).__init__(formdata, obj, prefix, **kwargs)

    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoArgumentsWrapper(formdata)
        super(Form, self).process(formdata, obj, **kwargs)

    def _get_translations(self):
        if not hasattr(self, '_locale_code'):
            self._locale_code = 'en_US'
        return TornadoLocaleWrapper(self._locale_code)

    @classmethod
    def populate_from_model(klass, model, ignore=[]):
        """
        Populates a form from a model, if you want to ignore some fields, use the ``ignore`` list (of strings)
        to set which fields not to be iterated over.
        """
        temp_data = dict(model)
        if '_id' in temp_data.keys():
            #Need to get rid of _id as it clashes with WTForms
            temp_data['id'] = temp_data['_id']
            del temp_data['_id']

        for key in ignore:
            if key in temp_data.keys():
                del temp_data[key]

        return klass(**temp_data)

    def populate_model_from_data(self, modelObj, ignore = []):
        """
        Will populate a model from the data provided by a form. Use the ``ignore`` list (must all be strings) to
        ignore data keys passed back by your form.
        """
        formData = self.data
        if 'id' in formData:
            del formData['id']

        for key, value in formData.iteritems():
            if key not in ignore:
                setattr(modelObj, key, value)

        return modelObj


class TornadoArgumentsWrapper(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def getlist(self, key):
        try:
            values = []
            for v in self[key]:
                v = to_unicode(v)
                if isinstance(v, unicode):
                    v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
                values.append(v)
            return values
        except KeyError:
            raise AttributeError


class TornadoLocaleWrapper(object):
    def __init__(self, code):
        self.locale = tornado.locale.get(code)

    def gettext(self, message):
        return self.locale.translate(message)

    def ngettext(self, message, plural_message, count):
        return self.locale.translate(message, plural_message, count)


from Mojo.ObjectMapper.ModelPrototype import EXCLUSIONS
from wtforms.form import BaseForm
from wtforms.fields import *
from wtforms import validators
import inspect

fieldMap = {'StringField':TextField,
            'IntegerField':IntegerField,
            'BooleanField':BooleanField,
            'FloatField':FloatField,
            'ListField':TextField,
            'ObjectIDField':HiddenField,
            'DateTimeField':DateTimeField}

def model_as_form(model, initObj=None, ignore=[], override={}):
    """
    Will take a model (non instantiated) object and produce a ``WTForm`` Form instance, this function only works one-way.

    ``model_as_form`` can take three parameters:

    - ``initObj`` - If you want to inittialise the form with data, pass it an instance of the model in question and it will do it's best to instantiate it
    - ``ignore`` - If you want to exclude a list of fields from the automated conversion you can specify them as a list of strings corresponding to the name of the field in your model
    - ``override`` - To specify a custom wtForm field type, pass these as a dictionary of ``{"field name":FieldType,}``

    *note*: The override function takes either classes or instantiated objects, so if you want to pass through custom validators
     as part of the override, simply specify them in the override as if you would in a standard Form definition.

     **Usage:** ::

        from Mojo.Forms.MojoFormHelper import model_as_form

        # Let's get some data from our imaginary blog app
        posts = yield gen.Task(BlogPost.find_async, {'published':True}, sort=[('date_published',1)])
        a_post = posts[0]

        # Define a custom override set, the first is a base class,
        # the second is an instance with my custom validators:

        overrides = {'post_body': TextAreaField,
                     'post_intro': TextAreaField('Your intro text', [validators.required(),
                                                                     validators.length(max=10)]}

        # Create the form - we will ignore tags and
        # comments (these are Lists, and not implemented),
        # and override with our custom fields (StringFields are by
        # default TextFields, but we want TextAreas):

        thisForm = model_as_form(BlogPost, initObj=a_post, ignore=['tags', 'comments'], override=overrides)

        # ...Now do something with the form

     The system will automatically transform required model fields to required Form fields, no other validation checks are
     passed through yet.

     For the 'friendly name' o your form field, Mojo will use the ``friendly`` Mojo Model Form parameter, if none is present,
     Mojo will use the name of the Modle Field.

    """
    if model:
        form_fields = {}

        if not initObj:
            ignore.append('_id')

        class_attrs = [attr for attr in model.__dict__ if '__' not in attr]

        for c in class_attrs:
            if c not in EXCLUSIONS:
                form_validators = []
                field_type = type(model.__dict__[c]).__name__
                field_name = str(c)

                if model.__dict__[c].friendly == '':
                    friendly_name = model.__name__
                else:
                    friendly_name = unicode(model.__dict__[c].friendly)

                if model.__dict__[c].allow_empty:
                    form_validators.append(validators.required())

                new_form_field = None
                if field_name not in ignore:
                    if field_name not in override.keys():
                        if field_type in fieldMap.keys():
                            new_form_field = fieldMap[field_type](friendly_name, form_validators)
                        else:
                            raise NotImplementedError('This field (%s) has not been implemented, please add it manually using override.' % field_type)
                    else:
                        #Now for some magic, this makes sure overrides can provide field instances and custom validators
                        if inspect.isclass(override[field_name]):
                            #instantiate a fresh object
                            new_form_field = override[field_name](friendly_name, form_validators)
                        else:
                            #Pass everything through
                            new_form_field = override[field_name]

                    if new_form_field:
                        if field_name == '_id': field_name ='id'
                        form_fields[field_name] = new_form_field

        new_form = BaseForm(form_fields)

        if initObj:
            temp_data = dict(initObj)
            if '_id' in temp_data.keys():
                #Need to get rid of _id as it clashes with WTForms
                temp_data['id'] = temp_data['_id']
                del temp_data['_id']

            for key, value in temp_data.iteritems():
                if key not in ignore:
                    new_form[key].data = value

        return new_form
    else:
        return None







