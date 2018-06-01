import time
import os

from app.libs import handlers
from app.libs import decorators
from app.models import items_model
from app.libs import photo
import config_web


# 新增商品信息、商品分类、按分类查询商品 API，以及对商品发表评价 API
class ApiGetItemInfoHandler(handlers.ApiBaseHandler):
    def get(self):
        current_page = self.get_argument('page', 1)
        data_list = items_model.Items.get_items_list_for_api(current_page)
        self.data['status'] = 'success'
        self.data['data'] = data_list
        self.write(self.data)


class ApiGetCategoriesHandler(handlers.ApiBaseHandler):
    def get(self):
        data_list = items_model.Categories.get_categoreis_for_api()
        self.data['status'] = 'success'
        self.data['data'] = data_list
        self.write(self.data)


class ApiFilterItemHandler(handlers.ApiBaseHandler):
    def get(self):
        categorie_id = self.get_argument('categorie_id')
        current_page = self.get_argument('page', 1)
        data_list = items_model.Items. \
            get_items_by_categorie_id(categorie_id, current_page)
        self.data['status'] = 'success'
        self.data['data'] = data_list
        self.write(self.data)


class ApiCreateCommentHandler(handlers.ApiBaseHandler):
    def get(self):
        form_data = self._build_form_data()
        new_time = int(time.time())
        form_data['create_time'] = new_time
        comment_obj = items_model.ItemComments.create_item_comment(form_data)
        files = self.request.files
        comment_image_list = []
        if files:
            for i in files:
                file_obj = files[i]
                server_file_path = '/static/photos'
                file_dir = os.path.join(
                    config_web.settings_common['static_path'],
                    'photos'
                )
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                data = photo.save_upload_photo(
                    file_obj[0],
                    file_dir,
                    server_file_path,
                    'comment'
                )
                if data:
                    data['comment_id'] = comment_obj.comment_id
                    comment_image_list.append(data)
        items_model.CommentImages.create_many_comment_image(comment_image_list)
        self.data['status'] = 'success'
        self.write(self.data)

    def _list_form_keys(self):
        return [
            'member_id', 'item_id', 'comment_content'
        ]