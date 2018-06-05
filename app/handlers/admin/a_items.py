import os
import uuid
import json
import time

from app.libs import decorators
from app.libs import handlers
from app.models import items_model
from app.libs import photo
import config_web


# /items_manage
class AdminItemsManageHandler(handlers.SiteBaseHandler):
    """
    商品表页面
    """
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page', 1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = (items_model.Items.item_name == value)
            item_list = items_model.Items.get_list_items(current_page, search_value)
            item_count = items_model.Items.get_items_count(search_value)
        else:
            item_list = items_model.Items.get_list_items(current_page)
            item_count = items_model.Items.get_items_count()
        uri = self.get_uri()
        specifications_type_dict = dict(items_model.Items. \
            specifications_type_choices)
        brand_dict = items_model.Brands.get_brands_list_for_all()
        categories_dict = items_model.Categories.get_all_categoreis_dict()
        self.render(
            'admin/a_items.html',
            item_obj = item_list, 
            item_obj_count = item_count,
            current_page = current_page,
            filter_args = filter_args,
            uri = uri,
            search_value = value,
            specifications_type_dict = specifications_type_dict,
            brand_dict = brand_dict,
            categories_dict = categories_dict,
        )


# /j/delete_item/
class AdminJsDeleteItemHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        item_id_list = self.get_arguments('item_id_list[]')
        for i in item_id_list:
            items_model.Items.update_item_by_itemid(i, {'status': 'deleted'})
        self.data['result'] = 'success'
        self.write(self.data)


# /image_manage/
class AdminImageManageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        item_id = self.get_argument('item_id')
        item =  items_model.Items.get_item_by_itemid(item_id)
        items_image_list = items_model.ItemImages.get_images_by_itemid(item_id)
        image_dict = {}
        for i in items_image_list:
            if i.image_type not in image_dict:
                image_dict[i.image_type] = [
                    {'image_path': i.image_path, 'image_id': i.image_id}
                ]
            else:
                image_dict[i.image_type].append(
                    {'image_path': i.image_path, 'image_id': i.image_id}
                )
        self.render('admin/a_image_manage.html',
            item_obj = item,
            image_dict = image_dict)


# /j/add_image
class AdminJsAddImageHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        file_dict = self.request.files
        image_type = self.get_argument('image_type')
        image_type_dict = items_model.ItemImages.type_choces
        image_type_dict = dict(image_type_dict)
        item_id = self.get_argument('item_id')
        # with ThreadPoolExecutor(max_workers=10) as pool:
        for k in file_dict:
            server_file_path = '/static/photos'
            file_dir = os.path.join(
                config_web.settings_common['static_path'],
                'photos'
            )
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            data = photo.save_upload_photo(
                file_dict[k][0],
                file_dir,
                server_file_path,
                image_type_dict.get(int(image_type))
            )
            if data:
                data.update({
                    'image_type': image_type,
                    'item_id': item_id,
                    'status': 'normal'
                })
                items_model.ItemImages.create_item_image(data)
            else:
                self.data['message'] = '上传失败'
                self.write(self.data)
                return
        else:
            self.data['result'] = 'success'
            self.write(self.data)
        

# /j/delete_image/
class AdminJsDeleteImageHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        image_id_list = self.get_arguments('image_id_list[]')
        image_type = items_model.ItemImages.type_choces
        image_type = dict(image_type)
        for i in image_id_list:
            image_obj = items_model.ItemImages.get_by_id(i)
            image_name = image_obj.image_path.rsplit('/', 1)[1]
            file_base_path = os.path.join(
                config_web.settings_common['static_path'],
                'photos',
                image_type.get(image_obj.image_type)
            )
            file_path = os.path.join(file_base_path, image_name)
            new_file_name = os.path.join(file_base_path, uuid.uuid4().hex + '.jpg')
            if os.path.exists(file_path):
                os.rename(file_path, new_file_name)
            items_model.ItemImages.update_image_by_image_id(i, {'status': 'deleted'})
            
        self.data['result'] = 'success'
        self.write(self.data)


# /add_item/
class AdminAdditemHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self._render()
    
    @decorators.admin_authenticated
    def post(self):
        form_data = self._build_form_data()
        form_error = self._validate_form_data(form_data)
        if form_error:
            self._render(form_data, form_error)
            return
        new_form_data = { key: form_data[key] \
            for key in form_data if form_data[key] }
        if new_form_data:
            new_form_data.update({
                "create_person": self.current_user.member_name,
                "create_time": int(time.time()),
                "update_time": int(time.time()),
            })
            items_model.Items.create_item(new_form_data)
            self.redirect('/items_manage/')

    def _list_form_keys(self):
        return [
            "item_name", "item_info", "item_code",
            "item_barcode", "price", "current_price",
            "foreign_price", "key_word", "origin",
            "shelf_life", "capacity", "specifications_type_id",
            "for_people", "weight", "brand_id",
            "categories_id"
        ]
    
    def _validate_form_data(self, form_data):
        form_error = dict()
        if not form_data['item_name']:
            form_error['item_name'] = '不能为空'
        return form_error
    
    def _render(self, form_data=None, form_errors=None):
        specifications_type_dict = dict(items_model.Items. \
            specifications_type_choices)
        brands_list = items_model.Brands.get_brands_list_for_all()
        categories_list = items_model.Categories.get_all_categoreis_dict()
        self.render(
            "admin/a_add_item.html",
            form_data = form_data,
            form_errors = form_errors,
            specifications_type_dict = specifications_type_dict,
            brands_list = brands_list,
            categories_list = categories_list
        )


# /editor_item/
class AdminEditorItemHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        item_id = self.get_argument('item_id')
        item_obj = items_model.Items.get_item_by_itemid(item_id)
        form_data = self._build_form_data()
        data = { key: getattr(item_obj, key) for key in form_data }
        self._render(data)

    @decorators.admin_authenticated
    def post(self):
        item_id = self.get_argument('item_id', None)
        form_data = self._build_form_data()
        back_url = self.get_argument('back_url', '/items_manage/')
        new_form_data = { i:form_data[i] for i in form_data if form_data[i] }
        if new_form_data:
            new_form_data['update_person'] = self.current_user.member_name
            new_form_data['update_time'] = int(time.time())
            items_model.Items.update_item_by_itemid(item_id, new_form_data)
            self.redirect(back_url)
    
    def _list_form_keys(self):
        return [
            "item_name", "item_info", "item_code",
            "item_barcode", "price", "current_price",
            "foreign_price", "key_word", "origin",
            "shelf_life", "capacity", "specifications_type_id",
            "for_people", "weight", "brand_id",
            "categories_id"
        ]
    
    def _render(self, form_data=None, form_errors=None):
        specifications_type_dict = dict(items_model.Items. \
            specifications_type_choices)
        brands_list = items_model.Brands.get_brands_list_for_all()
        categories_list = items_model.Categories.get_all_categoreis_dict()
        self.render(
            "admin/a_editor_item.html",
            form_data = form_data,
            form_errors = form_errors,
            specifications_type_dict = specifications_type_dict,
            brands_list = brands_list,
            categories_list = categories_list
        )


class AdminBrandsManageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page',1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = (items_model.Brands.cn_name == value)
            brands_list = items_model.Brands.get_list_brands(current_page, search_value)
            brands_count = items_model.Brands.get_brands_count(search_value)
        else:
            brands_list = items_model.Brands.get_list_brands(current_page)
            brands_count = items_model.Brands.get_brands_count()
        uri = self.get_uri()
        self.render(
            'admin/a_brands_manage.html',
            search_value = value,
            filter_args = filter_args,
            brands_list = brands_list,
            brands_count = brands_count,
            uri = uri,
            current_page = current_page
        )


class AdminAddbrandHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self._render()
    
    @decorators.admin_authenticated
    def post(self):
        form_data = self._build_form_data()
        form_error = self._validate_form_data(form_data)
        if form_error:
            self._render(form_error, form_data)
            return

        files = self.request.files
        if files:
            file_obj = files.get('f_brand_image')
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
                'brand'
            )
            if data:
                brand_image = data['image_path']
                form_data.update({'brand_image': brand_image})
        items_model.Brands.create_brand(form_data)
        self.redirect('/brands_manage/')
    
    def _list_form_keys(self):
        return [
            'cn_name', 'cn_name_abridge', 'en_name',
            'form_country', 'key_word', 'brand_about'
        ]
    
    def _validate_form_data(self, form_data):
        form_error = dict()
        if not form_data['cn_name']:
            form_error['cn_name'] = '至少这个不能为空'
        return form_error
    
    def _render(self, form_error=None, form_data=None):
        self.render(
            'admin/a_add_brand.html',
            form_error = form_error,
            form_data = form_data
        )


# /j/delete_brands/
class AdminJsDeleteBrandHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        brand_ids_list = self.get_arguments('brand_ids_list[]')
        for i in brand_ids_list:
            items_model.Brands.delete_by_id(i)
        self.data['result'] = 'success'
        self.write(self.data)


# /editor_brand/
class AdminEditorBrandHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        brand_id = self.get_argument('brand_id')
        brand_obj = items_model.Brands.get_brand_by_brandid(brand_id)
        form_data = items_model.Brands.obj_to_dict(brand_obj)
        self._render(form_data=form_data)
    
    @decorators.admin_authenticated
    def post(self):
        brand_id = self.get_argument('brand_id', None)
        back_url = self.get_argument('back_url', '/brands_manage/')
        form_data = self._build_form_data()
        new_form_data = { i:form_data[i] for i in form_data if form_data[i] }
        files = self.request.files
        if files:
            file_obj = files.get('f_brand_image')
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
                'brand'
            )
            if data:
                brand_image = data['image_path']
                new_form_data.update({'brand_image': brand_image})
        if new_form_data:
            items_model.Brands.update_brand_by_brandid(brand_id, new_form_data)
            self.redirect(back_url)
    
    def _render(self, form_error=None, form_data=None, brand_obj=None):
        self.render(
            'admin/a_add_brand.html',
            form_error = form_error,
            form_data = form_data,
            brand_obj = brand_obj
        )
    
    def _list_form_keys(self):
        return [
            'cn_name', 'cn_name_abridge', 'en_name',
            'form_country', 'key_word', 'brand_about'
        ]


# /categories_manage/
class AdminCategoriesManageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page', 1)
        value = self.get_argument('search_value', None)
        filter_args = None
        categorie_choices = dict(items_model.Categories.type_choices)
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = items_model.Categories.categorie_name == value
            categories_list = items_model.Categories. \
                get_list_categories(current_page, search_value)
            categories_count = items_model.Categories. \
                get_categories_count(search_value)
        else:
            categories_list = items_model.Categories. \
                get_list_categories(current_page)
            categories_count = items_model.Categories. \
                get_categories_count()
        self.render(
            "admin/a_categories_manage.html",
            search_value = value,
            categories_list = categories_list,
            current_page = current_page,
            categories_count = categories_count,
            filter_args = filter_args,
            uri = self.get_uri(),
            categorie_choices = categorie_choices
        )
    

# /add_categorie/
class AdminAddCategorieHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        self._render()

    @decorators.admin_authenticated
    def post(self):
        form_data = self._build_form_data()
        form_error = self._validate_form_data(form_data)
        if form_error:
            self._render(form_data, form_error)
            return
        files = self.request.files
        if files:
            file_obj = files.get('f_categorie_image')
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
                'brand'
            )
            if data:
                image_path = data['image_path']
                form_data.update({'image_path': image_path})
        items_model.Categories.create_new_categories(form_data)
        self.redirect("/categories_manage/")

    
    def _list_form_keys(self):
        return [
            'categorie_name', 'categorie_type',
        ]

    def _validate_form_data(self, form_data):
        form_errors = dict()
        if not form_data['categorie_name']:
            form_errors['categorie_name'] = '分类名不能为空'
        if not form_data['categorie_type']:
            form_errors['categorie_type'] = '请选择类别'
        return form_errors

    def _render(self, form_data=None, form_error=None):
        categorie_choices = dict(items_model.Categories.type_choices)
        self.render(
            'admin/a_add_categorie.html',
            form_data = form_data,
            form_error = form_error,
            categorie_choices = categorie_choices,
        )


#/editor_categorie/
class AdminEditorCategorieHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        categorie_id = self.get_argument('categorie_id')
        data = items_model.Categories.get_categorie_by_id(categorie_id)
        form_data = self._build_form_data()
        new_form_data = { key: getattr(data, key) for key in form_data }
        self._render(new_form_data)
    
    @decorators.admin_authenticated
    def post(self):
        categorie_id = self.get_argument('categorie_id')
        back_url = self.get_argument('back_url', '/categories_manage/')
        form_data = self._build_form_data()
        form_error = self._validate_form_data(form_data)
        if form_error:
            self._render(form_data, form_error)
            return

        files = self.request.files
        if files:
            file_obj = files.get('f_categorie_image')
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
                'brand'
            )
            if data:
                image_path = data['image_path']
                form_data.update({'image_path': image_path})
        new_form_data = { key: form_data[key] for key in form_data if form_data[key] }
        items_model.Categories.update_categorie_bt_id(categorie_id, new_form_data)
        self.redirect(back_url)

    def _list_form_keys(self):
        return [
            'categorie_name', 'categorie_type', 'image_path'
        ]
    
    def _validate_form_data(self, form_data):
        form_errors = dict()
        if not form_data['categorie_name']:
            form_errors['categorie_name'] = '分类名不能为空'
        if not form_data['categorie_type']:
            form_errors['categorie_type'] = '请选择类别'
        return form_errors
    
    def _render(self, form_data=None, form_error=None):
        categorie_choices = dict(items_model.Categories.type_choices)
        self.render(
            'admin/a_add_categorie.html',
            form_data = form_data,
            form_error = form_error,
            categorie_choices = categorie_choices
        )


# /j/delete_categorie/
class AdminJsDeleteCategorieHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        categorie_ids_list = self.get_arguments('categorie_ids_list[]')
        for i in categorie_ids_list:
            items_model.Categories.delete_by_id(i)
        self.data['result'] = 'success'
        self.write(self.data)


# /item_comments_manage/
class AdminItemCommentsManageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        current_page = self.get_argument('page', 1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = items_model.Items.item_name == value
            item_comments_list = items_model.ItemComments. \
                get_item_comments_list(current_page, search_value)
            count = items_model.ItemComments. \
                get_item_comments_count(search_value)
        else:
            item_comments_list = items_model.ItemComments. \
                get_item_comments_list(current_page)
            count = items_model.ItemComments.get_item_comments_count()
        self.render(
            'admin/a_item_comments_manage.html',
            current_page = current_page,
            search_value = value,
            filter_args = filter_args,
            item_comments_list = item_comments_list,
            count = count,
            uri = self.get_uri(),
        )


# /j/delete_comments/
class AdminJsDeleteCommentHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        comment_ids_list = self.get_arguments('comment_ids_list[]')
        for i in comment_ids_list:
            items_model.ItemComments.update_item_comment_by_id({'status': 'deleted'}, i)
        self.data['result'] = 'success'
        self.write(self.data)


# /editor_comment/
class AdminEditorCommentHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        comment_id = self.get_argument('comment_id')
        comment_obj = items_model.ItemComments.get_item_comment_dict_by_id(comment_id)
        self._render(form_data=comment_obj)
    
    @decorators.admin_authenticated
    def post(self):
        comment_id = self.get_argument('comment_id')
        back_url = self.get_argument('back_url')
        data = self._build_form_data()
        items_model.ItemComments.update_item_comment_by_id(data, comment_id)
        self.redirect(back_url)
        
    def _render(self, form_data=None, form_error=None):
        self.render(
            'admin/a_editor_comment.html',
            form_data = form_data,
            form_error = form_error,
        )
    
    def _list_form_keys(self):
        return [
            'comment_content',
        ]


# /comment_image_manage/
class AdminItemCommentImageHandler(handlers.SiteBaseHandler):
    @decorators.admin_authenticated
    def get(self):
        comment_id = self.get_argument('comment_id')
        comment_image_obj = items_model.CommentImages.get_comment_image_obj_by_id(comment_id)
        self.render(
            'admin/a_editor_comment_image.html',
            comment_image_list = comment_image_obj
        )
    

# /j/delete_item_comment_image/
class AdminJsDeleteCommentImageHandler(handlers.JsSiteBaseHandler):
    @decorators.js_authenticated
    def post(self):
        image_id_list = self.get_arguments('image_id_list[]')
        for i in image_id_list:
            items_model.CommentImages.update_comment_image_by_id(i, {'status': 'deleted'})
        self.data['result'] = "success"
        self.write(self.data)
    