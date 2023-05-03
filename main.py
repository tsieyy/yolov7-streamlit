import app
import app_test
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth



hashed_passwords = stauth.Hasher(['abc']).generate()

# print(hashed_passwords)

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('User Login', 'main')
# # 重置密码
# if authentication_status:
#     try:
#         if authenticator.reset_password(username, 'Reset password'):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)
# # 注册
# try:
#     if authenticator.register_user('Register user', preauthorization=False):
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)

# 登录
if authentication_status:
    # with st.container():
    #     cols1,cols2 = st.columns(2)
    #     cols1.write('欢迎 *%s*' % (name))
    #     with cols2.container():
    #         authenticator.logout('注销', 'main')

    app_test.main(authenticator)
elif authentication_status == False:
    st.error('用户名或密码不正确')
elif authentication_status == None:
    st.warning('请输入你的用户名或者密码')


