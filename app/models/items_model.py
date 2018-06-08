
import peewee

from app.models import base_model
from app.models import member_model
from app.libs import common
from playhouse.shortcuts import model_to_dict

class Brands(base_model.BaseModel):
    brand_id                    = peewee.AutoField(db_column="brand_id", primary_key=True, verbose_name="品牌ID")
    cn_name                     = peewee.CharField(db_column="cn_name", verbose_name="品牌中文名")
    cn_name_abridge             = peewee.CharField(db_column="cn_name_abridge", null=True, verbose_name="品牌中文名缩写")
    en_name                     = peewee.CharField(db_column="en_name", null=True, verbose_name="品牌英文名")
    form_country                = peewee.CharField(db_column="form_country", null=True, verbose_name="所属国家")
    key_word                    = peewee.CharField(db_column="key_word", null=True, verbose_name="搜索关键字")
    brand_about                 = peewee.CharField(db_column="brand_about", null=True, verbose_name="品牌简介")
    brand_image                 = peewee.CharField(db_column="brand_image", null=True, verbose_name="品牌图片路径")


    class Meta:
        db_table = "app_brands"
    
    
    @classmethod
    def create_brand(cls, datas):
        cls.create(**datas)
    
    @classmethod
    def get_list_brands(cls, current_page, search_value=None):
        if search_value:
            brand_obj = cls.select().where(search_value). \
                order_by(-cls.brand_id).paginate(int(current_page), 15)
        else:
            brand_obj = cls.select().order_by(-cls.brand_id).paginate(int(current_page), 15)
        
        return brand_obj
    
    @classmethod
    def get_brands_count(cls, search_value=None):
        if search_value:
            obj_count = cls.select().where(search_value).count()
        else:
            obj_count = cls.select().count()
        
        return obj_count
    
    @classmethod
    def get_brand_by_brandid(cls, brand_id):
        try:
            return cls.get(cls.brand_id == brand_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_brand_by_brandid(cls, brand_id, data):
        cls.update(**data).where(cls.brand_id == brand_id).execute()

    @classmethod
    def get_brands_list_for_all(cls):
        data_dict = dict()
        all_data = cls.select(cls.brand_id, cls.cn_name)
        if all_data:
            for i in all_data:
                data_dict[i.brand_id] = i.cn_name
        return data_dict


class Items(base_model.BaseModel):
    item_id                     = peewee.AutoField(db_column="item_id", primary_key=True, verbose_name='商品ID')
    item_name                   = peewee.CharField(db_column="item_name", verbose_name='商品名称')
    item_info                   = peewee.CharField(db_column="item_info", null=True, verbose_name='商品信息')
    item_code                   = peewee.CharField(db_column="item_code", null=True, verbose_name="商品编码")
    item_barcode                = peewee.CharField(db_column="item_barcode", null=True, verbose_name="商品条码")
    price                       = peewee.FloatField(db_column="price", null=True, verbose_name="商品原价")
    current_price               = peewee.FloatField(db_column='current_price', null=True, verbose_name="商品现价")
    foreign_price               = peewee.FloatField(db_column='foreign_price', null=True, verbose_name="国外价格")
    comment_count               = peewee.IntegerField(db_column="comment_count", null=True, verbose_name="评论数量")
    hot_value                   = peewee.IntegerField(db_column="hot_value", null=True, verbose_name="热度值")
    buy_count                   = peewee.IntegerField(db_column="buy_count", null=True, verbose_name="被购买次数")
    key_word                    = peewee.CharField(db_column="key_word", null=True, verbose_name="搜索关键字")
    origin                      = peewee.CharField(db_column="origin", null=True,  verbose_name="生产地")
    shelf_life                  = peewee.CharField(db_column="shelf_life", null=True, verbose_name="保质期")
    capacity                    = peewee.CharField(db_column="capacity", null=True, verbose_name="容量")
    specifications_type_choices = (
        (0, '瓶'),
        (1, '包'),
        (2, '套'),
        (3, '片'),
        (4, '支'),
        (5, '袋'),
        (6, '对'),
        (7, '盒')
    )
    specifications_type_id      = peewee.SmallIntegerField(db_column="specifications_type_id", choices=specifications_type_choices, null=True, verbose_name="规格类型")
    categories_id               = peewee.BigIntegerField(db_column="categories_id", null=True, verbose_name="分类ID")
    brand_id                    = peewee.BigIntegerField(db_column="brand_id", null=True, verbose_name="品牌ID")
    for_people                  = peewee.CharField(db_column="for_people", null=True, verbose_name="适用人群")
    weight                      = peewee.CharField(db_column="weight", null=True, verbose_name="重量")
    create_person               = peewee.CharField(db_column="create_person", verbose_name="创建人")
    create_time                 = peewee.IntegerField(db_column="create_time", verbose_name="创建时间")
    update_person               = peewee.CharField(db_column="update_person", null=True, verbose_name="更新人")
    update_time                 = peewee.IntegerField(db_column="update_time", verbose_name="更新时间")
    status                      = peewee.CharField(db_column="status", verbose_name="状态", default="normal")
    
    
    class Meta:
        db_table = "app_items"


    @classmethod
    def create_item(cls, datas):
        cls.create(**datas)
    
    @classmethod
    def get_item_by_itemid(cls, item_id):
        try:
            return cls.get(
                (cls.item_id == item_id) & (cls.status == 'normal')
            )
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_item_by_itemid(cls, item_id, item_dict):
        cls.update(**item_dict).where(cls.item_id == item_id).execute()

    @classmethod
    def get_list_items(cls, current_page, search_value=None):
        if search_value:
            item_obj = cls.select().where(
                (search_value) & (cls.status == 'normal')
            ).order_by(-cls.item_id).paginate(int(current_page), 15)
        else:
            item_obj = cls.select().where(cls.status == 'normal'). \
                order_by(-cls.item_id).paginate(int(current_page), 15)
        return item_obj
    
    @classmethod
    def get_items_count(cls, search_value=None):
        if search_value:
            item_obj_count = cls.select().where(
                (search_value) & (cls.status == 'normal')
            ).count()
        else:
            item_obj_count = cls.select().where(cls.status == 'normal').count()
        return item_obj_count

    @classmethod
    def get_items_all_select(cls):
        items = cls.select(cls.item_id, cls.item_name). \
            where(cls.status == 'normal').dicts()
        return items
    
    @classmethod
    def get_items_list_for_api(cls, current_page):
        item_obj = cls.select().order_by(-cls.item_id). \
            where(cls.status == 'normal'). \
            paginate(int(current_page), 15).dicts()
        item_obj = list(item_obj)
        for i in item_obj:
            image_obj = ItemImages.get_images_by_itemid(i['item_id']).dicts()
            image_obj = list(image_obj)
            i['image_list'] = image_obj
            icon_obj = ItemImages.get_thumbicon_by_item_id(i['item_id'])
            if icon_obj:
                i['item_thumbicon'] = model_to_dict(icon_obj)
        return item_obj

    @classmethod
    def get_items_by_categorie_id(cls, categorie_id, current_page):
        item_obj = cls.select().order_by(-cls.item_id). \
            where(
                (cls.categories_id == categorie_id) & (cls.status == 'normal')
            ).paginate(int(current_page), 15).dicts()
        item_obj = list(item_obj)
        for i in item_obj:
            image_obj = ItemImages.get_images_by_itemid(i['item_id']).dicts()
            image_obj = list(image_obj)
            i['image_list'] = image_obj
            icon_obj = ItemImages.get_thumbicon_by_item_id(i['item_id'])
            if icon_obj:
                i['item_thumbicon'] = model_to_dict(icon_obj)
        return item_obj


class ItemImages(base_model.BaseModel):
    image_id       = peewee.AutoField(db_column="image_id", primary_key=True, verbose_name="图片ID")
    item_id        = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    type_choces    = (
        (0, "title"),
        (1, "thumbicon"),
        (2, "item_title"),
        (4, "item"),
    )
    image_type      = peewee.IntegerField(db_column="image_type", choices=type_choces, verbose_name="图片类型")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="file_size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型")
    status          = peewee.CharField(db_column="status", verbose_name="状态")
    
    
    class Meta:
        db_table = "app_item_images"


    @classmethod
    def create_item_image(cls, datas):
        cls.create(**datas)

    @classmethod
    def get_images_by_itemid(cls, item_id, search_value = None):
        try:
            image_obj = cls.select().where((cls.item_id == item_id) & (cls.status == "normal"))
            return image_obj
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_image_by_image_id(cls, image_id, item_dict):
        cls.update(**item_dict).where(cls.image_id == image_id).execute()

    @classmethod
    def get_thumbicon_by_item_id(cls, item_id):
        try:
            image_obj = cls.get(
                (cls.item_id == item_id) & (cls.status == "normal") & (cls.image_type == 1)
            )
            return image_obj
        except cls.DoesNotExist:
            return None
    

class ItemTags(base_model.BaseModel):
    tag_id          = peewee.AutoField(db_column="tag_id", verbose_name="标签ID")
    tag_name        = peewee.CharField(db_column="tag_name", verbose_name="标签名")
    item_id         = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    
    
    class Meta:
        db_table = "app_item_tags"


class Categories(base_model.BaseModel):
    categorie_id    = peewee.AutoField(db_column="categorie_id", verbose_name="分类ID")
    categorie_name  = peewee.CharField(db_column="categorie_name", verbose_name="分类名")
    type_choices    = (
        (0, '功效专区'),
        (1, '基础护理'),
        (2, '个性彩妆'),
        (3, '营养保健')
    )
    categorie_type  = peewee.SmallIntegerField(db_column="categorie_type", choices=type_choices, null=True, verbose_name="类别")
    image_path      = peewee.CharField(db_column="image_path", null=True, verbose_name="缩略图路径")

    class Meta:
        db_table = "app_categories"


    @classmethod
    def get_list_categories(cls, current_page, search_value=None):
        if search_value:
            obj = cls.select().where(search_value). \
                order_by(-cls.categorie_id).paginate(int(current_page), 15)
        else:
            obj = cls.select().order_by(-cls.categorie_id).paginate(int(current_page), 15)
        return obj
    
    @classmethod
    def get_categories_count(cls, search_value=None):
        if search_value:
            count = cls.select().where(search_value).count()
        else:
            count = cls.select().count()
        return count
    
    @classmethod
    def create_new_categories(cls, data):
        cls.create(**data)
    
    @classmethod
    def get_categorie_by_id(cls, categorie_id):
        return cls.get_by_id(categorie_id)
    
    @classmethod
    def update_categorie_bt_id(cls, categorie_id, data):
        cls.update(**data).where(cls.categorie_id == categorie_id).execute()

    @classmethod
    def get_all_categoreis_dict(cls):
        dict_data = dict()
        all_obj =  cls.select(cls.categorie_id, cls.categorie_name)
        if all_obj:
            dict_data = { i.categorie_id: i.categorie_name for i in all_obj }
        return dict_data
    
    @classmethod
    def get_categoreis_for_api(cls):
        data_list = list()
        for i in cls.type_choices:
            temp = cls.select().where(cls.categorie_type == i[0]).dicts()
            temp = list(temp)
            data_list.append({i[1]: temp})
        return data_list


class ItemComments(base_model.BaseModel):
    comment_id      = peewee.AutoField(db_column="comment_id", verbose_name="评论ID")
    member_id       = peewee.BigIntegerField(db_column="member_id", verbose_name="评论用户ID")
    item_id         = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    comment_content = peewee.CharField(max_length=255, db_column="comment_content", verbose_name="评论内容")
    # reply_id        = peewee.BigIntegerField(db_column="reply_id", null=True, verbose_name="回复的评论ID")
    create_time     = peewee.IntegerField(db_column="create_time", verbose_name="创建时间")
    status          = peewee.CharField(db_column="status", verbose_name="状态", default="normal")


    class Meta:
        db_table = "app_item_comments"
    

    @classmethod
    def create_item_comment(cls, data):
        return cls.create(**data)

    @classmethod
    def get_item_comments_list(cls, current_page, search_value=None):
        if search_value:
            item_comments_list = cls.select(cls, Items, member_model.Member). \
                join(
                    Items, on = (cls.item_id == Items.item_id).alias('items')
                ).switch(cls).join(
                    member_model.Member,
                    on = (
                        cls.member_id == member_model.Member.member_id
                    ).alias('members')
                ).where(
                    (search_value) & (cls.status == 'normal')
                ).order_by(cls.comment_id).paginate(int(current_page), 15)
        else:
            item_comments_list = cls.select(cls, Items, member_model.Member). \
                join(
                    Items, on = (cls.item_id == Items.item_id).alias('items')
                ).switch(cls).join(
                    member_model.Member,
                    on = (
                        cls.member_id == member_model.Member.member_id
                    ).alias('members')
                ).where(cls.status == 'normal').paginate(int(current_page), 15)
        return item_comments_list
    
    @classmethod
    def get_item_comments_count(cls, search_value=None):
        count = None
        if search_value:
            count = cls.select(cls, Items).join(
                Items, on=(cls.item_id == Items.item_id)
            ).where((search_value) & (cls.status == 'normal')).count()
        else:
            count = cls.select().where(cls.status == 'normal').count()
        return count

    @classmethod
    def get_item_comment_dict_by_id(cls, comment_id):
        try:
            comment_obj = cls.select(ItemComments, Items.item_name). \
                join(Items, on = (cls.item_id == Items.item_id).alias('items')). \
                where(
                    (cls.comment_id == comment_id) & (cls.status == 'normal')
                ).dicts()
            return list(comment_obj)[0]
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_item_comment_data_by_item_id(cls, item_id, current_page):
        try:
            item_comments_list = cls.select(cls, member_model.Member.member_name). \
                join(
                    member_model.Member,
                    on = (
                        cls.member_id == member_model.Member.member_id
                    ).alias('members')
                ).where(
                    (cls.item_id == item_id) & (cls.status == 'normal')
                ).order_by(cls.comment_id).paginate(int(current_page), 15).dicts()
            item_comments_list = list(item_comments_list)
            for i in item_comments_list:
                image_list = list(CommentImages.get_comment_image_obj_by_id(i['comment_id']))
                i['image_list'] = image_list
            return item_comments_list
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_item_comment_by_id(cls, data, comment_id):
        cls.update(**data).where(cls.comment_id == comment_id).execute()

class CommentImages(base_model.BaseModel):
    image_id        = peewee.AutoField(db_column="image_id", verbose_name="图片ID")
    comment_id      = peewee.BigIntegerField(db_column="comment_id", verbose_name="所属评论ID")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="file_size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型", default='.jpg')
    status          = peewee.CharField(db_column="status", verbose_name="状态", default="normal")


    class Meta:
        db_table = "app_comment_images"
    

    @classmethod
    def create_many_comment_image(cls, data_list):
        for i in data_list:
            cls.create(**i)
    
    @classmethod
    def get_comment_image_obj_by_id(cls, comment_id):
        return cls.select().where(
            (cls.comment_id == comment_id) & (cls.status == 'normal')
        ).dicts()

    @classmethod
    def update_comment_image_by_id(cls, image_id, data):
        cls.update(**data).where(cls.image_id == image_id).execute()




def obj_to_dict(obj):
    data = model_to_dict(obj)
    return data