
def create_html_table(t_heads_data, tbodys_data):
    thead_str = "<thead><tr>"
    for i in t_heads_data:
        thead_str += "<th>{0}</th>".format(i)
    else:
        thead_str += "</tr></thead>"
    tbody_str = "<tbody>"
    for i in tbodys_data:
        tbody_str += "<tr>"
        for j in i:
            tbody_str += "<td>{0}</td>".format(j)
        tbody_str += "</tr>"
    else:
        tbody_str += "/tbody"
    return thead_str + tbody_str



class Pagingfunc:
	def __init__(self, current_page, all_count, data_num=None, show_page=None, url=None, filter_args=None):
		try:
			self.current_page = int(current_page)
		except:
			self.current_page = 1
		self.data_num = 10 if data_num is None else data_num
		a, b = divmod(all_count, self.data_num)
		if b:
			a = a + 1
		self.show_page = 10 if show_page is None else show_page
		self.all_page = a
		self.url = url if url != None else 'index'
		self.filter_args = filter_args if filter_args != None else ''


	def create_page_btn(self):
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
			previous = "<li><a href='#'>上一页<span aria-hidden='true'>&laquo;</span></a></li>"
		else:
			previous = "<li><a page=%s class='page_btn'>上一页<span aria-hidden='true'>&laquo;</span></a></li>" % (self.current_page - 1)
		html_list.append(previous)
		for i in range(start, stop + 1):
			if self.current_page == i:
				temp = """<li><a page=%s class='page_btn' style='background-color:yellowgreen;'>%s</a></li>""" % (i, i)
			else:
				temp = "<li><a page=%s class='page_btn'>%s</a></li>" % (i, i)
			html_list.append(temp)
		if self.current_page >= self.all_page:
			nex = "<li><a href='#'>下一页<span aria-hidden='true'>&raquo;</span></a></li>"
		else:
			nex = "<li><a page=%s class='page_btn'>下一页<span aria-hidden='true'>&raquo;</span></a></li>" % (self.current_page + 1)
		html_list.append(nex)
		return ''.join(html_list)