#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/18 2:08 PM
@desc:
'''
import os
import shutil

from flask import Flask, request, redirect, url_for , Blueprint
from flask import render_template
from werkzeug.utils import secure_filename
from app.echoImg import echoImg
from app.echoImg.boxDrawing import imgDrawBoxes



# UPLOAD_FOLDER = os.getcwd()+'/echoImg/static/uploads'
UPLOAD_FOLDER = os.getcwd()+'/app/echoImg/static/uploads'

print ("os.getcwd=%s  " %os.getcwd())
print ("UPLOAD_FOLDER=%s  " %UPLOAD_FOLDER)

# UPLOAD_FOLDER = 'app/static/uploads'
# ALLOWED_EXTENSIONS = set(['xml', 'jpg', 'jpeg','zip'])

bp = Blueprint('main', __name__,template_folder='templates' , static_folder='static')

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/imgDrawBox')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

XML_PATH = os.path.join(app.config['UPLOAD_FOLDER'], "xml")
JPG_PATH = os.path.join(app.config['UPLOAD_FOLDER'], "jpg")
RESULT_PATH = os.path.join(app.config['UPLOAD_FOLDER'], "result")
ZIP_PATH = os.path.join(app.config['UPLOAD_FOLDER'], "zip")





@echoImg.route('/picList', methods=['GET', 'POST'])
def picList():
    imgs = getPageImgList()
    return render_template('picList.html',imgs=imgs)



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


@echoImg.route('/batchDrawBoxes', methods=['POST'])
def batchDrawBoxes():

    if request.method == 'POST':
        imgs = getPageImgList()
        for imgInfo in imgs:

            resultName = imgInfo['resultName']
            imgName = imgInfo['imgName']
            xmlName = imgInfo['xmlName']
            if  not resultName.strip()  and  imgName.strip() and  xmlName.strip() :
                img_name = imgName.split('.')[0]
                print('drawBoxes：%s' % imgName)
                imgDrawBoxes(app.config['UPLOAD_FOLDER'], img_name)

        imgs = getPageImgList()

        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html', imgs=imgs)





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

        imgs = getPageImgList()
        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html', imgs=imgs)


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

        imgs = getPageImgList()


        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html',imgs=imgs)


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

        imgs = getPageImgList()

        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html', imgs=imgs)

@echoImg.route('/boxDrawing', methods=[ 'POST'])
def boxDrawing():
    if request.method == 'POST':
        imgName = request.form['imgName']
        img_name = imgName.split('.')[0]
        imgDrawBoxes(app.config['UPLOAD_FOLDER'],img_name)

        imgs = getPageImgList()

        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html', imgs=imgs)

def getAllowedExtensions(fileType):
    switcher = {
        "jpg": set(["jpg","jpeg"]),
        "xml": set(["xml"]),
        "zip": set(["zip"]),
    }
    return switcher.get(fileType, set([]))

@echoImg.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        fileType = request.form['type']

        if file and allowed_file(file.filename,getAllowedExtensions(fileType)):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],fileType, filename))

        imgs = getPageImgList()
        # return redirect(url_for('index', imgs=imgs))
        return render_template('index.html', imgs=imgs)




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


def getPageImgList():
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
    return imgs


def allowed_file(filename,allowedExtensions):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowedExtensions


@echoImg.route('/', methods=['GET', 'POST'])
def index():
    imgs = getPageImgList()
    return render_template('index.html',imgs=imgs)
    # return render_template('index.html')