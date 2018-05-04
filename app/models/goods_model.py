from app.models import base_model
import peewee



class Goods(base_model.BaseModel):
    goods_id        = peewee.AutoField(db_column="goods_id", primary_key=True, verbose_name='商品ID')
    goods_name      = peewee.CharField(db_column="goods_name", verbose_name='商品名称')
    goods_uuid      = peewee.CharField(db_column="goods_uuid", default='', verbose_name="商品识别码")
    goods_info      = peewee.CharField(db_column="goods_info", default='', verbose_name='商品信息')
    price           = peewee.FloatField(db_column="price", default=0, verbose_name="商品原价")
    current_price   = peewee.FloatField(db_column='current_price', default=0, verbose_name="商品现价")
    foreign_price   = peewee.FloatField(db_column='foreign_price', default=0, verbose_name="国外价格")
    comment_count   = peewee.IntegerField(db_column="comment_count", default=0, verbose_name="评论数量")
    hot_value       = peewee.IntegerField(db_column="hot_value", default=0, verbose_name="热度值")
    buy_count       = peewee.IntegerField(db_column="buy_count", default=0, verbose_name="被购买次数")
    key_word        = peewee.CharField(db_column="key_word", default="", verbose_name="搜索关键字")
    origin          = peewee.CharField(db_column="origin", default="",  verbose_name="生产地")
    shelf_life      = peewee.CharField(db_column="shelf_life", default="", verbose_name="保质期")
    capacity        = peewee.CharField(db_column="capacity", default="", verbose_name="容量")
    for_people      = peewee.CharField(db_column="for_people", default="", verbose_name="适用人群")
    weight          = peewee.CharField(db_column="weight", default="", verbose_name="重量")
    create_person   = peewee.CharField(db_column="create_person", verbose_name="创建人")
    create_time     = peewee.DateTimeField(db_column="create_time", verbose_name="创建时间")
    update_persom   = peewee.CharField(db_column="update_person", default="", verbose_name="更新人")
    update_time     = peewee.CharField(db_column="update_time", verbose_name="更新时间")



class GoodsImage(base_model.BaseModel):
    image_id        = peewee.AutoField(db_column="image_id", primary_key=True, verbose_name="图片ID")
    googs_id        = peewee.BigIntegerField(db_column="goods_id", verbose_name="所属商品ID")
    type_choces     = (
        (0, "首页图片"),
        (1, "商品缩略图"),
        (2, "商品样式图"),
        (3, "图文详情图"),
        (4, "商品详细介绍图"),
    )
    image_type      = peewee.IntegerField(db_column="image_type", choices=type_choces, verbose_name="图片类型")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型")



class GoodsTag(base_model.BaseModel):
    tag_id          = peewee.AutoField(db_column="tag_id", verbose_name="标签ID")
    tag_name        = peewee.CharField(db_column="tag_name", verbose_name="标签名")
    googs_id        = peewee.BigIntegerField(db_column="goods_id", verbose_name="所属商品ID")



class GoodsComment(base_model.BaseModel):
    comment_id      = peewee.AutoField(db_column="tag_id", verbose_name="评论ID")
    member_id       = peewee.BigIntegerField(db_column="member_id", verbose_name="评论用户ID")
    goods_id        = peewee.BigIntegerField(db_column="goods_id", verbose_name="所属商品ID")
    comment_content = peewee.CharField(max_length=255, db_column="comment_content", verbose_name="评论内容")
    reply_id        = peewee.BigIntegerField(db_column="reply_id", null=True, verbose_name="回复的评论ID")
    create_time     = peewee.DateTimeField(db_column="create_time", verbose_name="创建时间")



class CommentImage(base_model.BaseModel):
    image_id        = peewee.AutoField(db_column="tag_id", verbose_name="图片ID")
    comment_id      = peewee.BigIntegerField(db_column="comment_id", verbose_name="所属评论ID")
    image_path      = peewee.CharField(db_column="image_path", verbose_name="路径")
    file_size       = peewee.CharField(db_column="size", verbose_name="文件大小")
    resolution      = peewee.CharField(db_column="resolution", verbose_name="分辨率")
    file_type       = peewee.CharField(db_column="file_type", verbose_name="文件类型")



