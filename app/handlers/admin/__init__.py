from app.handlers.admin import a_account
from app.handlers.admin import a_walcome
import tornado.web
from tornado import escape

urls = [
    (r"/?",                                 a_walcome.AdminHomeHandler),
    (r"/member_manage/?",                   a_walcome.MemberManage),
	(r"/items_manage/?",					a_walcome.AdminItemsManageHandler),
    (r"/signin/?",                          a_account.AdminSigninHandler),
    (r"/signout/?",                         a_account.AdminSignoutHandler),
    (r"/register/?",                        a_account.AdminRegisterHandler),
    (r"/change_password/?",                 a_account.AdminChangePasswordHandler),
	
]

urls += [
    # (r"/j/member_info/?",          a_walcome.AdminJsMemberInfoHandler),
    (r"/j/register_member/?",      a_walcome.AdminJsRegisterMemberHandler),
    (r"/j/delete_member/?",        a_walcome.AdminJsDeleteMemberHandler),
    (r"/j/edit_member/?",          a_walcome.AdminJsEditMemberHandler),
	(r"/j/add_item/?",			   a_walcome.AdminJsAddItemHandler),
]



class Pagingfunc(tornado.web.UIModule):
	"""
	用于生成html页面分页按钮的类
	"""
	
	def render(self, current_page, all_count, filter_args, url=None):
		try:
			self.current_page = int(current_page)
		except:
			self.current_page = 1
		self.data_num = 15
		a, b = divmod(all_count, self.data_num)
		if b:
			a = a + 1
		self.show_page = 10
		self.all_page = a
		self.url = url if url != None else 'index'
		self.filter_args = filter_args if filter_args != None else ''
		html_list = []
		half = int((self.show_page - 1) / 2)
		start = 0
		stop = 0
		if self.all_page < self.show_page:
			start = 1
			stop = self.all_page
		else:
			if self.current_page < half + 1:
				start = 1
				stop = self.show_page
			else:
				if self.current_page >= self.all_page - half:
					start = self.all_page - 10
					stop = self.all_page
				else:
					start = self.current_page - half
					stop = self.current_page + half
		if self.current_page <= 1:
			previous = "<li><a href='#' style='cursor:pointer;text-decoration:none;'>上一页<span aria-hidden='true'>&laquo;</span></a></li>"
		else:
			previous = "<li><a href='%s?page=%s%s' class='page_btn'  style='cursor:pointer;text-decoration:none;'>上一页<span aria-hidden='true'>&laquo;</span></a></li>" % (self.url, self.current_page - 1, self.filter_args)
		html_list.append(previous)
		for i in range(start, stop + 1):
			if self.current_page == i:
				temp = """<li><a href='%s?page=%s%s' class='page_btn' style='background-color:yellowgreen;cursor:pointer;text-decoration:none;'>%s</a></li>""" % (self.url, i, self.filter_args, i)
			else:
				temp = "<li><a href='%s?page=%s%s' class='page_btn' style='cursor:pointer;text-decoration:none;'>%s</a></li>" % (self.url, i, self.filter_args, i)
			html_list.append(temp)
		if self.current_page >= self.all_page:
			nex = "<li><a href='#' style='cursor:pointer;text-decoration:none;'>下一页<span aria-hidden='true'>&raquo;</span></a></li>"
		else:
			nex = "<li><a href='%s?page=%s%s' class='page_btn' style='cursor:pointer;text-decoration:none;'>下一页<span aria-hidden='true'>&raquo;</span></a></li>" % (self.url, self.current_page + 1, self.filter_args)
		html_list.append(nex)
		return ''.join(html_list)
        