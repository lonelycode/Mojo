import tornado.web

class Entry(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string(
            "UI_modules/module_entry.html", entry=entry)