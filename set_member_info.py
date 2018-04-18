
from hashlib import md5
import datetime
import json

# sessions = json.dumps(list())
phone = '1050434689'
# password = '123'
# has_pwd = md5(password.encode(encoding='utf8')).hexdigest()
from app.models.member_model import Member


# Member.create(password =has_pwd,
#             telephone = phone,
#             member_id = phone,
#             email = phone,
#             status = '1',
#             create_time=datetime.datetime.now(),
#             sessions=sessions,
#             role='root')

obj = Member.get(member_id=phone)
obj.role='admin'
obj.save()