import tornado.web
from tornado import escape

from app.handlers.admin import a_account
from app.handlers.admin import a_walcome
from app.handlers.admin import a_member
from app.handlers.admin import a_items
from app.models import items_model


urls = [
    (r"/?",                                 a_walcome.AdminHomeHandler),
    (r"/member_manage/?",                   a_member.AdminMemberManageHandler),
	(r"/items_manage/?",					a_items.AdminItemsManageHandler),
	(r"/image_manage/?",					a_items.AdminImageManageHandler),
	(r"/add_item/?",						a_items.AdminAdditemHandler),
	(r"/editor_item/?",						a_items.AdminEditorItemHandler),
	(r"/brands_manage/?",					a_items.AdminBrandsManageHandler),
	(r"/add_brand/?",						a_items.AdminAddbrandHandler),
	(r"/editor_brand/?",					a_items.AdminEditorBrandHandler),
	(r"/categories_manage/?",				a_items.AdminCategoriesManageHandler),
	(r"/add_categorie/?",					a_items.AdminAddCategorieHandler),
	(r"/editor_categorie/?",				a_items.AdminEditorCategorieHandler),
    (r"/signin/?",                          a_account.AdminSigninHandler),
    (r"/signout/?",                         a_account.AdminSignoutHandler),
    (r"/register/?",                        a_account.AdminRegisterHandler),
    (r"/change_password/?",                 a_account.AdminChangePasswordHandler),
]

urls += [
    # (r"/j/member_info/?",          a_walcome.AdminJsMemberInfoHandler),
    (r"/j/register_member/?",      a_member.AdminJsRegisterMemberHandler),
    (r"/j/delete_member/?",        a_member.AdminJsDeleteMemberHandler),
    (r"/j/edit_member/?",          a_member.AdminJsEditMemberHandler),
	# (r"/j/add_item/?",			   a_items.AdminJsAddItemHandler),
	(r"/j/delete_item/?",		   a_items.AdminJsDeleteItemHandler),
	# (r"/j/edit_item/?",			   a_items.AdminJsEditItemHandler),
	(r"/j/add_image/?",			   a_items.AdminJsAddImageHandler),
	(r"/j/delete_image/?",		   a_items.AdminJsDeleteImageHandler),
	(r"/j/delete_brands/?",		   a_items.AdminJsDeleteBrandHandler),
	(r"/j/delete_categorie/?",	   a_items.AdminJsDeleteCategorieHandler),
]



class Pagingfunc(tornado.web.UIModule):
	"""
	用于生成html页面分页按钮的类
	"""
	
	def render(self, current_page, all_count, filter_args, uri=None):
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
		self.uri = uri if uri is not None else '/'
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
			previous = """
				<li>
				<a href='#' style='cursor:pointer;text-decoration:none;'>
				上一页<span aria-hidden='true'>&laquo;</span>
				</a>
				</li>
			"""
		else:
			previous = """
				<li>
				<a href='{0}?page={1}{2}' class='page_btn'  style='cursor:pointer;text-decoration:none;'>
				上一页<span aria-hidden='true'>&laquo;</span>
				</a>
				</li>
			""".format(self.uri, self.current_page - 1, self.filter_args)
		html_list.append(previous)
		for i in range(start, stop + 1):
			if self.current_page == i:
				temp = """
					<li>
					<a href='{0}?page={1}{2}' class='page_btn' style='background-color:yellowgreen;cursor:pointer;text-decoration:none;'>
					{3}
					</a>
					</li>
				""".format(self.uri, i, self.filter_args, i)
			else:
				temp = """
					<li>
					<a href='{0}?page={1}{2}' class='page_btn' style='cursor:pointer;text-decoration:none;'>
					{3}</a>
					</li>
				""".format(self.uri, i, self.filter_args, i)
			html_list.append(temp)
		if self.current_page >= self.all_page:
			nex = """
				<li>
				<a href='#' style='cursor:pointer;text-decoration:none;'>
				下一页<span aria-hidden='true'>&raquo;</span>
				</a>
				</li>
			"""
		else:
			nex = """
				<li>
				<a href='{0}?page={1}{2}' class='page_btn' style='cursor:pointer;text-decoration:none;'>
				下一页<span aria-hidden='true'>&raquo;</span>
				</a>
				</li>
			""".format(self.uri, self.current_page + 1, self.filter_args)
		html_list.append(nex)
		return ''.join(html_list)


class GetThumbiconById(tornado.web.UIModule):
	def render(self, item_id):
		item_image_obj = items_model.ItemImages.get_thumbicon_by_item_id(item_id)
		if item_image_obj:
			return item_image_obj.image_path
		else:
			return "/images/user-default.jpg"


ui_modules = {
    "Pagingfunc": Pagingfunc,
	"GetThumbiconById": GetThumbiconById
}
