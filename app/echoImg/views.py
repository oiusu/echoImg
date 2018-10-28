#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 2:08 PM
@desc:
'''
import os
import shutil

from flask import render_template, session
from flask import request
from werkzeug.utils import secure_filename, redirect

from app.echoImg import echoImg
from app.echoImg.boxDrawing import imgDrawBoxes

UPLOAD_FOLDER = os.getcwd()+'/echoImg/static/uploads'   # 本地
# UPLOAD_FOLDER = os.getcwd()+'/app/echoImg/static/uploads'  # 服务器

print ("os.getcwd=%s  " %os.getcwd())
print ("UPLOAD_FOLDER=%s  " %UPLOAD_FOLDER)



XML_PATH = os.path.join(UPLOAD_FOLDER, "xml")
JPG_PATH = os.path.join(UPLOAD_FOLDER, "jpg")
RESULT_PATH = os.path.join(UPLOAD_FOLDER, "result")
ZIP_PATH = os.path.join(UPLOAD_FOLDER, "zip")


def getUserXmlPath():
    return os.path.join(UPLOAD_FOLDER,session.get("username"), "xml")
def getUserJpgPath():
    return os.path.join(UPLOAD_FOLDER,session.get("username"), "jpg")
def getUserResultPath():
    return os.path.join(UPLOAD_FOLDER,session.get("username"), "result")
def getUserZipPath():
    return os.path.join(UPLOAD_FOLDER,session.get("username"), "zip")

def auth(func):
    def inner(*args,**kwargs):
        username = session.get("username")
        if username:
            print("[auth] username = %s" %username)
            return func(*args,**kwargs)
        else:
            print("[auth] username = %s" % username)
            return redirect("/echoImg/login")

    return inner


# 返回列表页面
@echoImg.route('/picList', methods=['GET', 'POST'])
def picList():
    imgs ,username = getPageParams()
    return render_template('picList.html',imgs=imgs,username=username)




# 批量结果生成
@echoImg.route('/batchDrawBoxes', methods=['POST'])
def batchDrawBoxes():

    if request.method == 'POST':
        imgs ,username  = getPageParams()
        for imgInfo in imgs:

            resultName = imgInfo['resultName']
            imgName = imgInfo['imgName']
            xmlName = imgInfo['xmlName']
            if  not resultName.strip()  and  imgName.strip() and  xmlName.strip() :
                # 当resultName为空且 imgName和xmlName 都存在的情况下，需要执行生成resultImg
                img_name = imgName.split('.')[0]
                print('drawBoxes：%s' % imgName)
                imgDrawBoxes(UPLOAD_FOLDER, img_name)

        return redirect("/echoImg")




# 批量上传压缩包 并且解压
@echoImg.route('/batchUploadAndUnzip', methods=['POST'])
def batchUploadAndUnzip():

    if request.method == 'POST':
        file = request.files['file']
        fileType = request.form['type']

        if file and allowed_file(file.filename,getAllowedExtensions(fileType)):
            # 清空zip目录
            shutil.rmtree(ZIP_PATH)
            os.mkdir(ZIP_PATH)

            filename = secure_filename(file.filename)

            zipFilePath = os.path.join(ZIP_PATH, filename)
            file.save(zipFilePath)
            #解压zip 内文件到 jpg xml 里
            shutil.unpack_archive(zipFilePath,ZIP_PATH)
            # 遍历所有文件 并移动
            recursionDir(ZIP_PATH)

            # 清空zip目录
            shutil.rmtree(ZIP_PATH)
            os.mkdir(ZIP_PATH)

        return redirect("/echoImg")


# 遍历zip_path 下 所有文件 并移动
def recursionDir(path):
    fs = os.listdir(path)
    for i in fs:
        tmp_path = os.path.join(path, i)
        if not os.path.isdir(tmp_path):

            if os.path.splitext(i)[1] == '.jpg':
                print("jpg : "+ i)
                if not os.path.exists(os.path.join(JPG_PATH,i)):
                    shutil.move(tmp_path, JPG_PATH)  # 移动文件
            if os.path.splitext(i)[1] =='.xml':
                print("xml : " + i)
                if not os.path.exists(os.path.join(XML_PATH,i)):
                    shutil.move(tmp_path, XML_PATH)  # 移动文件
        else:
            print('文件夹：%s' % tmp_path)
            recursionDir(tmp_path)

@echoImg.route('/deleteAll', methods=[ 'POST'])
def deleteAll():
    if request.method == 'POST':

        # 删除 jpg xml result


        shutil.rmtree(XML_PATH)
        os.mkdir(XML_PATH)

        shutil.rmtree(JPG_PATH)
        os.mkdir(JPG_PATH)

        shutil.rmtree(RESULT_PATH)
        os.mkdir(RESULT_PATH)

        return redirect("/echoImg")


@echoImg.route('/delete', methods=[ 'POST'])
def delete():
    if request.method == 'POST':
        imgName = request.form['imgName']
        imgNamePrefix = imgName.split('.')[0]

        # 删除 jpg xml result
        xml_file_path = os.path.join(XML_PATH, imgNamePrefix + '.xml')
        jpg_file_path = os.path.join(JPG_PATH, imgNamePrefix + '.jpg')
        result_file_path = os.path.join(RESULT_PATH, imgNamePrefix + '.jpg')
        if os.path.exists(xml_file_path):
            os.remove(xml_file_path)
        if os.path.exists(jpg_file_path):
            os.remove(jpg_file_path)
        if os.path.exists(result_file_path):
            os.remove(result_file_path)

        return redirect("/echoImg")

# 单个图片 结果生成
@echoImg.route('/boxDrawing', methods=[ 'POST'])
def boxDrawing():
    if request.method == 'POST':
        imgName = request.form['imgName']
        img_name = imgName.split('.')[0]
        imgDrawBoxes(UPLOAD_FOLDER,img_name)

        return redirect("/echoImg")

@echoImg.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        fileType = request.form['type']

        if file and allowed_file(file.filename,getAllowedExtensions(fileType)):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,fileType, filename))

        return redirect("/echoImg")

def allowed_file(filename,allowedExtensions):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowedExtensions

def getAllowedExtensions(fileType):
    switcher = {
        "jpg": set(["jpg","jpeg"]),
        "xml": set(["xml"]),
        "zip": set(["zip"]),
    }
    return switcher.get(fileType, set([]))

def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,  key=lambda x: os.path.getctime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list


def getPageParams():
    # 获得目录下的图片列表 按上传时间排序
    list = get_file_list(JPG_PATH)

    imgs = []

    if  list :
        for i in range(0, len(list)):
            imgName = list[i].split('.')[0]

            imgInfo = {
                'imgName': '',
                'xmlName': '',
                'resultName': ''
            }

            imgInfo['imgName'] = imgName + '.jpg'
            # 查看文件是否存在
            xml_file_path = os.path.join(XML_PATH, imgName + '.xml')
            if os.path.exists(xml_file_path):
                imgInfo['xmlName'] = imgName + '.xml'
            result_file_path = os.path.join(RESULT_PATH, imgName + '.jpg')
            if os.path.exists(result_file_path):
                imgInfo['resultName'] = imgName + '.jpg'

            imgs.append(imgInfo)
    return imgs ,session.get("username")


@echoImg.route('/logout', methods=['GET'])
def logout():
    print("get logout")
    session.pop('username', None)
    # session 里删除
    return render_template('form.html')



@echoImg.route('/login', methods=['POST','GET'])
def login():
    if request.method == "GET":
        return render_template('form.html')
    else:

        username = request.form['username']
        password = request.form['password']
        if (username == 'admin' and password == '123') or (username == 'chenc' and password == '456'):
            session['username'] = username

            return redirect("/echoImg")
        return render_template('form.html', message='账号或密码错误', username=username)

#
# @echoImg.before_request
# def before_user():
#     if 'username' in session:
#         username = session.get("username")
#         return render_template('signin-ok.html', username=username)
#     else:
#         return render_template('form.html', message='未登录')



@echoImg.route('/homePage', methods=['GET'])
def homePage():
    return redirect("/echoImg")


@echoImg.route('/', methods=['GET'])
@auth
def index():
    imgs ,username = getPageParams()
    return render_template('index.html',imgs=imgs , username=username)
    # return render_template('index.html')


