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
        current_page = self.get_argument('page',1)
        value = self.get_argument('search_value', None)
        filter_args = None
        if value:
            filter_args = '&search_value={0}'.format(value)
            search_value = (items_model.Items.item_name == value)
            item_obj = items_model.Items.get_items_obj(current_page, search_value)
            item_obj_count = items_model.Items.get_items_obj_count(search_value)
        else:
            item_obj = items_model.Items.get_items_obj(current_page)
            item_obj_count = items_model.Items.get_items_obj_count()
        if '?' in self.request.uri:
            url = self.request.uri.split('?')[0]
        else:
            url = self.request.uri
        
        self.render('admin/a_items.html', item_obj = item_obj, 
                                          item_obj_count = item_obj_count,
                                          current_page = current_page,
                                          filter_args = filter_args,
                                          url = url,
                                          search_value = value,)


# /j/add_item/
class AdminJsAddItemHandler(handlers.JsSiteBaseHandler):
    """
    添加商品
    """
    def post(self):
        form_data = self._build_form_data()
        form_data.update({
            "create_person":self.current_user.member_name,
            "create_time":int(time.time()),
            "update_time":int(time.time()),
        })
        try:
            items_model.Items.create(**form_data)
            self.write(json.dumps({'status':True}))
        except Exception as error:
            self.write(json.dumps({"status":False,
            "error_msg":"服务器出错:\n{0}".format(str(error))}))

    def _list_form_keys(self):
        return ["item_name", "item_info", "item_code",
                "item_barcode", "price", "current_price",
                "foreign_price", "key_word", "origin",
                "shelf_life", "capacity", "for_people", "weight"]


# /j/delete_item/
class AdminJsDeleteItemHandler(handlers.JsSiteBaseHandler):
    def post(self):
        try:
            item_id_list = self.get_arguments('item_id_list[]')
            for i in item_id_list:
                items_model.Items.delete_by_id(i)
            self.write(json.dumps({'status':True}))
        except Exception as error:
            self.write(json.dumps({'status':False,
                                   'error_msg':'服务器出错：{0}'.format(str(error))}))


# /j/edit_item/
class AdminJsEditItemHandler(handlers.JsSiteBaseHandler):
    def get(self):
        item_id = self.get_argument('item_id', None)
        try:
            member_obj = items_model.Items.get_item_by_itemid(item_id)
            field = ["item_name", "item_info", "item_code",
                     "item_barcode", "price", "current_price",
                     "foreign_price", "key_word", "origin",
                     "shelf_life", "capacity", "for_people", "weight"]
            data_dict = {i:getattr(member_obj, i) for i in field if i != "more"}
            self.write(json.dumps({"status":True, "data":data_dict}))
        except Exception as error:
            self.write(json.dumps({"status":False,
                                   "error_msg":"服务器出错:{0}".format(str(error))}))
        
        
    
    def post(self):
            item_id = self.get_argument('item_id', None)
            form_data = self._build_form_data()
            new_form_data = { i:form_data[i] for i in form_data if form_data[i] }
            new_form_data['update_person'] = self.current_user.member_name
            new_form_data['update_time'] = int(time.time())
            if new_form_data:
                try:
                    items_model.Items.update_item_by_itemid(item_id, new_form_data)
                    self.write(json.dumps({"status":True}))
                except Exception as error:
                    self.write(json.dumps({"status":False,
                    "error_msg":"服务器出错:{0}".format(str(error))}))

        
    def _list_form_keys(self):
        return ["item_name", "item_info", "item_code",
                "item_barcode", "price", "current_price",
                "foreign_price", "key_word", "origin",
                "shelf_life", "capacity", "for_people", "weight"]




# /image_manage/
class AdminImageManageHandler(handlers.SiteBaseHandler):
    def get(self):
        item_id = self.get_argument('item_id')
        item_obj =  items_model.Items.get_item_by_itemid(item_id)
        items_image_obj = items_model.ItemsImage.get_images_by_itemid(item_id)
        image_dict = {}
        for i in items_image_obj:
            if i.image_type not in image_dict:
                image_dict[i.image_type] = [{'image_path':i.image_path,
                                             'image_id':i.image_id}]
            else:
                image_dict[i.image_type].append({'image_path':i.image_path,
                                                 'image_id':i.image_id})
        self.render('admin/a_image_manage.html', item_obj = item_obj,
                                                 image_dict = image_dict)
    
    def post(self):
        file_dict = self.request.files
        image_type = self.get_argument('image_type')
        image_type_dict = items_model.ItemsImage.type_choces
        image_type_dict = dict(image_type_dict)
        item_id = self.get_argument('item_id')
        # with ThreadPoolExecutor(max_workers=10) as pool:
        for k in file_dict:
            server_file_path = '/static/photos'
            file_dir = os.path.join(config_web.settings_common['static_path'], 'photos')
            if not os.path.exists(file_dir):os.mkdir(file_dir)
            data = photo.save_upload_photo(file_dict[k][0],
                                            file_dir,
                                            server_file_path,
                                            image_type_dict.get(int(image_type)))
            if data:
                data.update({
                    'image_type':image_type,
                    'item_id':item_id,
                })
                try:
                    items_model.ItemsImage.create(**data)
                except Exception as error:
                    self.write(json.dumps({'status':False,
                                           'error_msg':str(error)}))
                    break
            else:
                self.write(json.dumps({'status':False,
                                       'error_msg':"服务器出错：上传失败"}))
                return
        else:
            self.write(json.dumps({'status':True}))
        


# /j/delete_image/
class AdminJsDeleteImageHandler(handlers.JsSiteBaseHandler):
    def post(self):
        image_id_list = self.get_arguments('image_id_list[]')
        image_type = items_model.ItemsImage.type_choces
        image_type = dict(image_type)
        try:
            for i in image_id_list:
                image_obj = items_model.ItemsImage.get_by_id(i)
                image_name = image_obj.image_path.rsplit('/', 1)[1]
                file_base_path = os.path.join(config_web.settings_common['static_path'],
                                              'photos',
                                              image_type.get(image_obj.image_type))
                file_path = os.path.join(file_base_path, image_name)
                new_file_name = os.path.join(file_base_path, uuid.uuid4().hex + '.jpg')
                if os.path.exists(file_path):os.rename(file_path, new_file_name)
                items_model.ItemsImage.update_image_by_image_id(i, {'status':'deleted'})
            self.write(json.dumps({'status':True}))
        except Exception as error:
            self.write(json.dumps({'status':False,
                    'error_msg':'服务器出错：{0}'.format(str(error))}))