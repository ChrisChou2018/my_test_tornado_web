from app.libs import decorators
from app.libs import handlers
from app.models.member_model import Member
import json
# /
class AdminHomeHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self.render("admin/a_index.html")
        

class MemberManage(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self.render("admin/a_member_manage.html")





class AdminJsAddJobHandler(handlers.ApiBaseHandler):
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
