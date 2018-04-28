import re


class RegisterForm(object):
    def __init__(self):
        self.member_name = {'re':r"^.{0,15}$", 'msg':'长度不超过15'}
        self.email = {'re':r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", 'msg':'邮箱格式不正确'}
        self.password = {'re':r"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':r"^.{0,30}$", 'msg':'密码长 度不超过30'}
    
    def check_valid(self, form_data, is_edit = False):
        form_dict = self.__dict__
        clear_data = {}
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        if form_data.get('password') != form_data.get('password2'):
            return_data['error_msg'] = {'password':'两次密码不一致'}
        elif not form_data.get('password') or not form_data.get('password2'):
            if is_edit:
                pass
            else:
                return_data['error_msg'] = {'password':'密码不能为空'}
        elif not form_data.get('member_name'):
            if  is_edit:
                pass
            else:
                return_data['error_msg'] = {'member_name':'昵称不能为空'}
        elif not form_data.get('email'):
            if is_edit:
                pass
            else:
                return_data['error_msg'] = {'email':'邮箱不能为空'}
        if return_data['error_msg']:
            return_data['status'] = False
            return return_data
        for key, regular in form_dict.items():
            post_value = form_data.get(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            if post_value:
                ret = re.match(regular['re'], post_value)
                if not ret:
                    return_data['status'] = False
                    return_data['error_msg'] = {key:regular['msg']}
                    return return_data
                clear_data[key] = post_value
        else:
            return_data['clear_data'] = clear_data
            return return_data



class ChangePasswordForm(object):
    def __init__(self):
        self.password = {'re':r"^.{0,30}$", 'msg':'密码长度不超过30'}
        self.password2 = {'re':r"^.{0,30}$", 'msg':'密码长度不超过30'}
        
    def check_valid(self, form_data):
        form_dict = self.__dict__
        clear_data = {}
        return_data = {
            'clear_data':None,
            'error_msg':{},
            'status':True,
        }
        
        if not form_data.get('password') or not form_data.get('password2'):
            return_data['error_msg'] = {'password':'密码不能为空'}
        if return_data['error_msg']:
            return_data['status'] = False
            return return_data
        for key, regular in form_dict.items():
            post_value = form_data.get(key)
            # 让提交的数据 和 定义的正则表达式进行匹配
            ret = re.match(regular['re'], post_value)
            if not ret:
                return_data['status'] = False
                return_data['error_msg'] = {key:regular['msg']}
                return return_data
            clear_data[key] = post_value
        else:
            return_data['clear_data'] = clear_data
            return return_data
