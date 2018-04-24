from app.models.member_model import Member
myModels = [Member]
for myModel in myModels:
    myModel.create_table()
    