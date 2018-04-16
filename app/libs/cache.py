# coding:utf-8

import hashlib
import functools
try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis

import config_web


if config_web.settings["redis_on"]:
    r = redis.StrictRedis(host=config_web.redis_host, port=config_web.redis_port, db=0)
else:
    r = None


def _compute_key(function, args, kwargs):
    '''序列化并求其哈希值'''
    # key = pickle.dumps((function.func_name, args, kw))
    key = function.__name__ + repr(args) + repr(kwargs)
    return hashlib.sha1(key).hexdigest()
    # return hashlib.sha1(key).hexdigest()


def memorize(duration=config_web.settings["redis_expire_duration"]):
    '''自动缓存'''
    def _memoize(function):
        @functools.wraps(function)  # 自动复制函数信息
        def __memoize(*args, **kw):
            redis_on = config_web.settings["redis_on"]
            if redis_on:
                key = _compute_key(function, args, kw)
                #是否已缓存？
                if r.exists(key):
                    try:
                        return pickle.loads(r.get(key))
                    except:
                        pass
                # 运行函数
                result = function(*args, **kw)
                #保存结果
                r.set(key, pickle.dumps(result), ex=duration)
                return result
            else:
                result = function(*args, **kw)
                return result

        return __memoize
    return _memoize


def save_cache(key, value):
    """将对象 value 存储到redis"""
    duration = 60 * 5
    if config_web.settings["redis_on"]:
        r.set(key, pickle.dumps(value), ex=duration)

    return value

def get_cache(key):
    """将对象 value　存储到redis"""
    if config_web.settings["redis_on"]:
        if r.exists(key):
            try:  # 可能判断后刚好缓存失效
                return pickle.loads(r.get(key))
            except:
                return None

    return None
