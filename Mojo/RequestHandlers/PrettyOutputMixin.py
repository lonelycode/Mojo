#Modified version of Phil Plante's prettified output to work with a Mojo installation

#Source: http://tornadogists.org/911930/
# Copyright (c) 2011 Phil Plante <unhappyrobot AT gmail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import httplib
import logging
import os
import Mojo
from tornado.web import RequestHandler

exception_template = os.path.dirname(Mojo.__file__) + '/Resources/MojoTemplates/exception.html'

class UncaughtExceptionMixin(object):
    def get_error_html(self, status_code, **kwargs):
        def get_snippet(fp, target_line, num_lines):
            if fp.endswith('.html'):
                fp = os.path.join(self.get_template_path(), fp)

            half_lines = (num_lines/2)
            try:
                with open(fp) as f:
                    all_lines = [line for line in f]

                    return ''.join(all_lines[target_line-half_lines:target_line+half_lines])
            except Exception, ex:
                logging.error(ex)

                return ''

        if self.application.settings.get('debug', False) is False:
            full_message = kwargs.get('exception', None)
            if not full_message or unicode(full_message) == '':
                full_message = 'Sky is falling!'

            return "<html><title>%(code)d: %(message)s</title><body><h1>%(code)d: %(message)s</h1>%(full_message)s</body></html>" % {
                "code": status_code,
                "message": httplib.responses[status_code],
                "full_message": full_message,
                }
        else:
            exception = kwargs.get('exception', None)

            return self.render_string(exception_template, get_snippet=get_snippet, exception=exception, status_code=status_code, kwargs=kwargs)