from app.models.member_model import Member
import json
import datetime

for i in range(50):
    Member.create(**{
        'member_name':'chris2{0}'.format(i),
        'hash_pwd':'sssssssss',
        'email':'10504346{0}'.format(i),
        'status':'1',
        'role':'admin',
        'create_time':datetime.datetime.now(),
        'sessions':json.dumps(list()),
    })