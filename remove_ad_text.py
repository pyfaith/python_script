# -*- coding: utf-8 -*-
# Author: Faith
# email: pyfaith@foxmail.com
# Date: 2018/9/25
'''
移除给定目录下给定的广告词汇
'''
import os

def remove_or_add_adtext(dir2, adtext, default="remove"):
    '''移除给定路径下文件(目录)(dir2)中的广告词(adtext)

    :param dir2: str
        文件路径
    :param adtext: str
        广告词
    :param default: str
        remove/add
        默认处理方式为移除 adtext
    :return:
    '''
    #判断给定路径是否为目录, 不是目录直接返回
    if not os.path.isdir(dir2):
        return
    #判断文件给定路径文件分隔符
    if not dir2.endswith(os.path.sep):
        dir2 += os.path.sep
    #获取dir2目录下的所有文件, []类型 eg:['temp', 'a.py']
    names = os.listdir(dir2)
    #依次遍历文件(目录)除去广告词
    for name in names:
        #获取每个文件的完整的路径
        sub_path = os.path.join(dir2, name)
        #判读是否为目录, 是则递归依次操作,除去广告词
        if os.path.isdir(sub_path):
            remove_or_add_adtext(sub_path, adtext)

        if default == "add":
            name = "{}{}".format(adtext, name)
        else:
            name = name.replace(adtext, "")
        #获取除去广告词的文件的路径
        new_path = os.path.join(dir2, name)
        #重命名为除去广告词的文件
        os.rename(sub_path, new_path)


if __name__ == '__main__':
    remove_or_add_adtext(r"/tmp/test", "pyfaith.cn")