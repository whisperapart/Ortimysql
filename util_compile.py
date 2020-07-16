#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
@File:      util_compile.py
@Author:    Jim.Dai.Cn
@Date:      2020/6/24 下午11:58
@Desc:         
"""

import compileall
import py_compile
import os

if __name__ == '__main__':
    compileall.compile_dir(r'./JDLibs')
    # 创建 release 文件夹
    # 复制 libs 　pyc
    # 复制 main 文件
    # 删除 compile 文件
    # 打包为 zip

    if os.path.exists('./publish/'):
        os.system('rm -rf ./publish')
    if os.path.exists('./release/'):
        os.system('rm -rf ./release')
    os.system('rm -rf release.zip')
    os.system('rm -rf release.pyz')
    os.system('mkdir ./release')
    os.system('cp -r ./JDLibs/__pycache__ ./release/JDLibs')

    os.system('pip3 install -r requirements.txt --target release')

    fileList = os.listdir('./release/JDLibs/')
    for f in fileList:
        os.system("mv ./release/JDLibs/%s ./release/JDLibs/%s" % (f, f.replace('.cpython-37', '')))

    #py_compile.compile('./o2m.py')
    #os.system("mv ./__pycache__/1.cpython-37.pyc ./release/a.py")
    os.system("cp ./o2m.py ./release/a.py")
    os.system("cp ./syncInit.py ./release/b.py")

    # cleanups
    os.system('rm -rf ./JDLibs/__pycache__')
    os.system('rm -rf ./__pycache__')

    if os.path.exists('./publish/'):
        os.system('rm -rf ./publish')
    os.system('mkdir ./publish')

    os.system('python3 -m zipapp release -m "a:main"')
    os.system('mv release.pyz ./publish/o2md.pyz')
    os.system('python3 -m zipapp release -m "b:main"')
    os.system('mv release.pyz ./publish/o2k.pyz')

    if os.path.exists('./release/'):
        os.system('rm -rf ./release')
    # python -m zipapp release -m "a:main"
    # http://c.biancheng.net/view/2687.html


