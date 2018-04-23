
from hashlib import md5
import datetime
import json

sessions = json.dumps(list())
email = '1050434689@qq.com'
password = '123456'
has_pwd = md5(password.encode(encoding='utf8')).hexdigest()
member_name = 'ChrisChou'

from app.models.member_model import Member


Member.create(password =has_pwd,
            member_name = member_name,
            email = email,
            status = '1',
            create_time=datetime.datetime.now(),
            sessions=sessions,
            role='admin')

# obj = Member.get(member_id=phone)
# obj.role='admin'
# obj.save()