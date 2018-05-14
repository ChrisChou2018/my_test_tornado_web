from app.libs import decorators
from app.libs import handlers

# /
class AdminHomeHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self.render("admin/a_index.html")
    



