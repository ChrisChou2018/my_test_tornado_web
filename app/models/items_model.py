
import peewee

from app.models import base_model


class Items(base_model.BaseModel):
    item_id                     = peewee.AutoField(db_column="item_id", primary_key=True, verbose_name='商品ID')
    item_name                   = peewee.CharField(db_column="item_name", verbose_name='商品名称')
    item_info                   = peewee.CharField(db_column="item_info", default='', verbose_name='商品信息')
    item_code                   = peewee.CharField(db_column="item_code", default="", verbose_name="商品编码")
    item_barcode                = peewee.CharField(db_column="item_barcode", default="", verbose_name="商品条码")
    price                       = peewee.FloatField(db_column="price", default=0, verbose_name="商品原价")
    current_price               = peewee.FloatField(db_column='current_price', default=0, verbose_name="商品现价")
    foreign_price               = peewee.FloatField(db_column='foreign_price', default=0, verbose_name="国外价格")
    comment_count               = peewee.IntegerField(db_column="comment_count", default=0, verbose_name="评论数量")
    hot_value                   = peewee.IntegerField(db_column="hot_value", default=0, verbose_name="热度值")
    buy_count                   = peewee.IntegerField(db_column="buy_count", default=0, verbose_name="被购买次数")
    key_word                    = peewee.CharField(db_column="key_word", default="", verbose_name="搜索关键字")
    origin                      = peewee.CharField(db_column="origin", default="",  verbose_name="生产地")
    shelf_life                  = peewee.CharField(db_column="shelf_life", default="", verbose_name="保质期")
    capacity                    = peewee.CharField(db_column="capacity", default="", verbose_name="容量")
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
    for_people                  = peewee.CharField(db_column="for_people", default="", verbose_name="适用人群")
    weight                      = peewee.CharField(db_column="weight", default="", verbose_name="重量")
    create_person               = peewee.CharField(db_column="create_person", verbose_name="创建人")
    create_time                 = peewee.IntegerField(db_column="create_time", verbose_name="创建时间")
    update_person               = peewee.CharField(db_column="update_person", default="", verbose_name="更新人")
    update_time                 = peewee.IntegerField(db_column="update_time", verbose_name="更新时间")
    
    
    class Meta:
        db_table = "app_items"


    @classmethod
    def create_item(cls, datas):
        cls.create(**datas)
    
    @classmethod
    def get_item_by_itemid(cls, item_id):
        try:
            return Items.get(Items.item_id == item_id)
        except Items.DoesNotExist:
            return None

    @classmethod
    def update_item_by_itemid(cls, item_id, item_dict):
        Items.update(**item_dict).where(Items.item_id == item_id).execute()

    @classmethod
    def get_list_items(cls, current_page, search_value=None):
        if search_value:
            item_obj = Items.select().where(search_value).order_by(-Items.item_id).paginate(int(current_page), 15)
        else:
            item_obj = Items.select().order_by(-Items.item_id).paginate(int(current_page), 15)
        
        return item_obj
    
    @classmethod
    def get_items_count(cls, search_value=None):
        if search_value:
            item_obj_count = Items.select().where(search_value).count()
        else:
            item_obj_count = Items.select().count()
        
        return item_obj_count


class ItemsImage(base_model.BaseModel):
    image_id       = peewee.AutoField(db_column="image_id", primary_key=True, verbose_name="图片ID")
    item_id        = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    type_choces    = (
        (0, "title"),
        (1, "thumbicon"),
        (2, "item_title"),
        (3, "item_info"),
        (4, "item"),
    )
    image_type      = peewee.IntegerField(db_column="image_type", choices=type_choces, verbose_name="图片类型")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="file_size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型")
    status          = peewee.CharField(db_column="status", default="normal", verbose_name="状态")
    
    
    class Meta:
        db_table = "app_items_image"


    @classmethod
    def create_item_image(cls, datas):
        cls.create(**datas)

    @classmethod
    def get_images_by_itemid(cls, item_id, search_value = None):
        try:
            image_obj = ItemsImage.select().where((ItemsImage.item_id == item_id) & (ItemsImage.status == "normal"))
            return image_obj
        except Items.DoesNotExist:
            return None
    
    @classmethod
    def update_image_by_image_id(cls, image_id, item_dict):
        ItemsImage.update(**item_dict).where(ItemsImage.image_id == image_id).execute()
    

class ItemTag(base_model.BaseModel):
    tag_id          = peewee.AutoField(db_column="tag_id", verbose_name="标签ID")
    tag_name        = peewee.CharField(db_column="tag_name", verbose_name="标签名")
    item_id         = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    
    
    class Meta:
        db_table = "app_item_tag"


class ItemComment(base_model.BaseModel):
    comment_id      = peewee.AutoField(db_column="comment_id", verbose_name="评论ID")
    member_id       = peewee.BigIntegerField(db_column="member_id", verbose_name="评论用户ID")
    item_id         = peewee.BigIntegerField(db_column="item_id", verbose_name="所属商品ID")
    comment_content = peewee.CharField(max_length=255, db_column="comment_content", verbose_name="评论内容")
    reply_id        = peewee.BigIntegerField(db_column="reply_id", null=True, verbose_name="回复的评论ID")
    create_time     = peewee.IntegerField(db_column="create_time", verbose_name="创建时间")


    class Meta:
        db_table = "app_item_comment"


class CommentImage(base_model.BaseModel):
    image_id        = peewee.AutoField(db_column="image_id", verbose_name="图片ID")
    comment_id      = peewee.BigIntegerField(db_column="comment_id", verbose_name="所属评论ID")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="file_size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型")


    class Meta:
        db_table = "app_comment_image"


