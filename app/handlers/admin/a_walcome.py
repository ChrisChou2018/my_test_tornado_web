from app.libs.decorators import admin_authenticated
from app.libs.handlers import SiteBaseHandler, ApiBaseHandler
from app.models.member_model import Member
import json
# /
class AdminHomeHandler(SiteBaseHandler):
    @admin_authenticated
    def get(self):
        self.render("admin/a_index.html")
        

class MemberManage(SiteBaseHandler):
    @admin_authenticated
    def get(self):
        self.render("admin/a_member_manage.html")



def init_table(t_heads,tbodys):
    thead_str = "<thead><tr>"
    for i in t_heads:
        thead_str += "<th>{0}</th>".format(i)
    else:
        thead_str += "</tr></thead>"
    tbody_str = "<tbody>"
    for i in tbodys:
        tbody_str += "<tr>"
        for j in i:
            tbody_str += "<td>{0}</td>".format(j)
        tbody_str += "</tr>"
    else:
        tbody_str += "/tbody"
    return thead_str + tbody_str


class ApiMemberInfoHandler(ApiBaseHandler):
    def get(self):
        member_obj = Member.select()
        data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
        return_data = init_table(['member_id', 'member_name', 'email', 'role'], data_list)
        self.finish({'return_data':return_data})
        


class AdminJsAddJobHandler(ApiBaseHandler):
    def get(self):
        # import app.models.rq_model as rq_model
        # import app.workers.wms_worker as wms_worker
        # order_data = {"order_id":"32132132131", "warehouse_id":"1231231231"}
        # rq_model.enqueue_job(wms_worker.wms_push_order, order_data)
        import os
        import uuid
        from PIL import Image
        # import app.models.goods_model as goods_model
        # import app.libs.picture as lib_picture
        source_path = os.path.join(self.settings["static_path"], "..", "localfile")
