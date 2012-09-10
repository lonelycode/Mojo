from views import *

urlpatterns = [
    (r'/admin/login/', loginHandler),
    (r'/admin/logout/', logoutHandler),
    (r'/admin/', adminHomeHandler),
    (r'/admin/(w+)/', modelActionHandler),
]
