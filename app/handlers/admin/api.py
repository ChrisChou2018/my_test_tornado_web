from app.libs.decorators import admin_authenticated 
from app.libs.handlers import SiteBaseHandler
from app.models.member_model import Member
from app.libs.page_fuc import Pagefunc
import json


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


class ApiMemberInfoHandler(SiteBaseHandler):
    @admin_authenticated
    def get(self):
        return_data = {
            'data':None,
            'message':'',
            'status':True,
            'page':'',
        }
        try:
            current_page = self.get_argument('page')
        except:
            current_page = 1
        table_head = ['member_id', 'member_name', 'email', 'role']
        member_obj = Member.select().paginate(int(current_page), 10)
        member_obj_count = Member.select().count()
        page_obj = Pagefunc(current_page, member_obj_count)
        data_list = [[i.member_id, i.member_name, i.email, i.role] for i in member_obj]
        # self.set_header('Content-Type', 'application/json; charset=UTF-8')
        return_data['data'] = init_table(table_head, data_list)
        return_data['page'] = page_obj.page()
        self.write(json.dumps(return_data))
        