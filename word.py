import os
from PIL import Image
import streamlit as st

f_path = os.path.join('dataset', 'assert')

def showInfo():
    st.header('作品简介:')
    st.write('本团队设计了一个基于YOLOv7的船舶识别系统，该系统能够在复杂的情况下对海上船舶进行检测识别和目标跟踪。由于海上光线和环境的变化，常常出现识别不准确和跟踪不稳定的情况。因此，本团队设计的系统采用了最新的深度学习算法和高质量的图像数据集，能够有效地克服这些困难。本系统采用YOLOv7算法，能够迅速准确地定位和识别船舶。此外，该系统还具备目标跟踪功能，能够实时跟踪船舶的位置和方向。')



def showFangan():
    st.header('系统技术方案图：')
    img3 = Image.open(os.path.join(f_path, '4.png'))
    st.image(img3, caption='系统技术方案图')


def showQuestion():
    st.header('本系统解决的痛点问题：')
    st.markdown('''
    本作品主要解决以下几个痛点问题:
    
    1. 海面上的情况十分复杂，天气、光照、海浪、潮汐等因素都会对船舶检测造成一定的难度。这些因素可能会导致船舶检测算法误检或漏检，进而影响船舶检测的精度和效率。
    2. 在海面上进行多船舶检测任务也存在困难。尽管船舶检测算法已经取得了很大的进展，但是在复杂环境下，例如天气恶劣、海浪汹涌、船舶密集等情况，船舶检测效果仍然较差，同时实时性也无法满足实际需求。
    ''')
    c1, c2 = st.columns(2)
    with c1:
        img1 = Image.open(os.path.join(f_path, '1.JPG'))
        st.image(img1, caption='海面船舶检测环境示例1')
    with c2:
        img2 = Image.open(os.path.join(f_path, '2.JPG'))
        st.image(img2, caption='海面船舶检测环境示例2')


def showInstance():
    st.header('数据集实例图：')
    img4 = Image.open(os.path.join(f_path, '3.jpg'))
    st.image(img4, caption='数据集实例图')


def showTrain():
    st.header('训练效果图：')
    img5 = Image.open(os.path.join(f_path, '5.jpg'))
    st.image(img5, caption='训练效果图')
    img6 = Image.open(os.path.join(f_path, '6.png'))
    st.image(img6, caption='训练损失值')




