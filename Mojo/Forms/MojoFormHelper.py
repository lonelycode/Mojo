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

#TODO: Create a model-to-form generator function, this will be the basis of an Admin app.