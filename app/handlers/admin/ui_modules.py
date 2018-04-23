import tornado.web
import app.libs.data as data

class AdminNavModule(tornado.web.UIModule):
    def render(self, tpl="admin/a_m_nav.html"):
        return self.render_string(tpl)


class AdminMenuModule(tornado.web.UIModule):
    def render(self, module_name, tpl="admin/a_m_menu.html"):
        permissions = data.role_permission[self.current_user.role]
        return self.render_string(tpl, module_name=module_name,
            permissions=permissions
        )


class AdminFooterModule(tornado.web.UIModule):
    def render(self, tpl="admin/a_m_footer.html"):
        return self.render_string(tpl)

ui_modules = {
    "AdminNavModule": AdminNavModule,
    "AdminMenuModule": AdminMenuModule,
    "AdminFooterModule": AdminFooterModule,
}