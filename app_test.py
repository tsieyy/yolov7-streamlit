import argparse

import streamlit as st
import torch
from detect import detect, source_code
# from detect_api import detectapi
from PIL import Image
from io import *
import glob
from datetime import datetime
import os
import wget
import time

## CFG
cfg_model_path = "best.pt"

cfg_enable_url_download = False
if cfg_enable_url_download:
    url = "https://archive.org/download/yoloTrained/yoloTrained.pt"  # Configure this if you set cfg_enable_url_download to True
    cfg_model_path = f"models/{url.split('/')[-1:][0]}"  # config model path from url name


parser = argparse.ArgumentParser()
parser.add_argument('--weights', nargs='+', type=str, default='best.pt', help='model.pt path(s)')
parser.add_argument('--source', type=str, default='dataset', help='source')  # file/folder, 0 for webcam
parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
parser.add_argument('--view-img', action='store_true', help='display results')
parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
parser.add_argument('--augment', action='store_true', help='augmented inference')
parser.add_argument('--update', action='store_true', help='update all models')
parser.add_argument('--project', default='runs/detect', help='save results to project/name')
parser.add_argument('--name', default='exp', help='save results to project/name')
parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
opt = parser.parse_args()


## END OF CFG


def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)




def imageInput(device, src):
    if src == '📀上传自己的数据':
        image_file = st.file_uploader("上传一张图片", type=['png', 'jpeg', 'jpg'])
        # col1, col2 = st.columns(2)
        if image_file is not None:
            img = Image.open(image_file)
            with st.container():
                st.image(img, caption='上传的图片', use_column_width='always')
            ts = datetime.timestamp(datetime.now())
            imgpath = os.path.join('dataset/uploads', str(ts) + image_file.name)
            # outputpath = os.path.join('dataset/outputs', os.path.basename(imgpath))
            with open(imgpath, mode="wb") as f:
                f.write(image_file.getbuffer())

            # call Model prediction--
            # model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yoloTrained.pt', force_reload=True)
            # model.cuda() if device == 'cuda' else model.cpu()
            opt.source = imgpath
            detect(opt)
            outputpath = os.path.join(get_detection_folder(), os.path.basename(imgpath))

            # --Display predicton

            img_ = Image.open(outputpath)
            with st.container():
                st.image(img_, caption='检测后的图片', use_column_width='always')

    elif src == '💿从测试集中选择':
        # Image selector slider
        imgpath = glob.glob('dataset/images/*')
        imgsel = st.slider('滑动滑块选择图片吧！', min_value=1, max_value=len(imgpath), step=1)
        image_file = imgpath[imgsel - 1]
        submit = st.button("开始检测！")
        # col1, col2 = st.columns(2, gap='small')
        with st.container():
            img = Image.open(image_file)
            st.image(img, caption='选择的图片', use_column_width='always')
        with st.container():
            if image_file is not None and submit:
                # call Model prediction--
                opt.source = image_file
                detect(opt)
                outputpath = os.path.join(get_detection_folder(), os.path.basename(image_file))

                # --Display predicton
                img_ = Image.open(outputpath)
                st.image(img_, caption='检测后的图片')
        # detect_info = st.container()
        # with detect_info:
        #     st.write("检测信息统计：")
        #     st.write("TODO....")



def videoInput(device, src):
    if src == '📀上传自己的数据':
        uploaded_video = st.file_uploader("上传视频", type=['mp4', 'mpeg', 'mov'])
        if uploaded_video != None:
            ts = datetime.timestamp(datetime.now())
            imgpath = os.path.join('dataset/uploads', str(ts) + uploaded_video.name)
            # outputpath = os.path.join('dataset/video_output', os.path.basename(imgpath))

            with open(imgpath, mode='wb') as f:
                f.write(uploaded_video.read())  # save video to disk

            st_video = open(imgpath, 'rb')
            video_bytes = st_video.read()
            st.write("上传的视频:")
            st.video(video_bytes)

            opt.source = imgpath
            with st.spinner('正在处理文件，请稍等...'):
                detect(opt)

            time.sleep(5)
            st.success('处理完成!')

            outputpath = os.path.join(get_detection_folder(), os.path.basename(imgpath))
            # print(outputpath)
            st_video2 = open(outputpath, 'rb')
            video_bytes2 = st_video2.read()
            st.write("检测后的视频:")
            st.video(video_bytes2)
    elif src == '💿从测试集中选择':
        imgpath = glob.glob('dataset/videos/*')
        imgsel = st.slider('滑动滑块选择视频吧！', min_value=0, max_value=len(imgpath), step=1)
        image_file = imgpath[imgsel - 1]
        c1, c2 = st.columns(2)
        with c1:
            submit = st.button("开始检测！")
        with c2:
            if image_file is not None and submit:
                with st.spinner('正在处理文件，请稍等...'):
                    time.sleep(5)
                st.success('处理完成!')


        col1, col2 = st.columns(2, gap='small')
        with col1:
            # img = Image.open(image_file)
            st_video = open(image_file, 'rb')
            video_bytes = st_video.read()
            st.write("上传的视频:")
            st.video(video_bytes)

        with col2:
            if image_file is not None and submit:
                # call Model prediction--
                opt.source = imgpath
                # time.sleep(5)
                outputpath = os.path.join('dataset', 'video_output', 'video0.mp4')
                # print(outputpath)
                st_video2 = open(outputpath, 'rb')
                video_bytes2 = st_video2.read()
                st.write("检测后的视频:")
                st.video(video_bytes2)




def cameraInput(device, src):
    ip_input = st.text_input("请输入摄像头IP地址！")
    ip_button = st.button("连接")
    if ip_input != None and ip_button:
        # 传入摄像头IP成功情况下
        st.error('IP无效！', icon="🚨")


# def webcamInput(device, src):



def showCode():
    st.subheader("👇检测函数源码：")
    st.markdown(source_code)


def start_detect(authenticator):
    datasrc = st.sidebar.radio("💾选择输入源", ['💿从测试集中选择', '📀上传自己的数据'])
    option = st.sidebar.radio("📲选择输入类型", ['📷图片', '🎬视频', '📹摄像头'])
    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("💻选择计算资源", ['cpu', 'cuda'], disabled=False, index=1)
    else:
        deviceoption = st.sidebar.radio("💻选择计算资源", ['cpu', 'cuda'], disabled=True, index=0)


    # -- End of Sidebar

    st.title('🚢“鹰眼护航”智能船舶检测系统🚢')
    st.markdown('---')
    # st.header('👈 选择左侧功能')
    # TODO 修改
    # st.sidebar.markdown("https://github.com/thepbordin/Obstacle-Detection-for-Blind-people-Deployment")
    if option == "📷图片":
        imageInput(deviceoption, datasrc)
    elif option == "🎬视频":
        videoInput(deviceoption, datasrc)
    elif option == "📹摄像头":
        cameraInput(deviceoption, datasrc)
    #  elif option == "🌎️网络视频":
    #      webcamInput(deviceoption, datasrc)




def main(authenticator):
    # -- Sidebar
    st.sidebar.title('⚙️选项')
    st.sidebar.write('👇请选择下列功能')
    select = st.sidebar.selectbox("🥰想要做点什么？", ['启动检测程序', '查看源代码'])
    # st.sidebar.markdown('---')
    if select == "启动检测程序":
        start_detect(authenticator)
    elif select == "查看源代码":
        showCode()

    st.sidebar.markdown('---')
    with st.sidebar:
        authenticator.logout('注销', 'main')



if __name__ == '__main__':

    main(opt)


