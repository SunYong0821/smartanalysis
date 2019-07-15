# coding=utf-8

import itchat
from itchat.content import *
import time
import re
import os

# TEXT         文本
# MAP          地图
# CARD         名片
# SHARING      分享
# PICTURE      图片/表情
# RECORDING    语音
# ATTACHMENT   附件
# VIDEO        小视频
# FRIENDS      好友邀请
# SYSTEM       系统消息
# NOTE         通知(消息撤回等)
# isFriendChat表示好友之间，isGroupChat表示群聊，isMapChat表示公众号

information = {}


@itchat.msg_register([TEXT, PICTURE, ATTACHMENT, RECORDING, VIDEO], isFriendChat=True, isGroupChat=True)
def receive_msg(msg):
    global face_bug
    receive_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if 'ActualNickName' in msg:
        user_id = msg['ActualUserName']
        ni_cheng = msg['ActualNickName']
        friends = itchat.get_friends(update=True)
        for f in friends:
            if user_id == f['UserName']:
                if f['RemarkName']:
                    ni_cheng = f['RemarkName']
                else:
                    ni_cheng = f['NickName']
                break
        groups = itchat.get_chatrooms(update=True)
        for g in groups:
            if msg['FromUserName'] == g['UserName']:
                group_name = g['NickName']
                group_members = g['MemberCount']
                break
        group_name = group_name + "(" + str(group_members) + ")"
    else:
        if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
            ni_cheng = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            ni_cheng = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        group_name = ""
    msg_time = msg['CreateTime']
    msg_id = msg['MsgId']
    msg_content = None
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']
        msg['Text'](str(msg_content))
    face_bug = msg_content
    time.sleep(2)
    information.update(
        {
            msg_id: {
                "ni_cheng": ni_cheng,
                "msg_time": msg_time,
                "receive_time": receive_time,
                "msg_type": msg["Type"],
                "msg_content": msg_content,
                "group_name": group_name
            }
        }
    )

    del_info = []
    for k in information:
        m_time = information[k]['msg_time']
        if int(time.time()) - m_time > 120:
            del_info.append(k)
    if del_info:
        for i in del_info:
            information.pop(i)


# 监听是否有消息撤回
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True)
def information(msg):
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search(r"\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = information.get(old_msg_id)
        if len(old_msg_id) < 11:
            itchat.send_file(face_bug, toUserName='filehelper')
        else:
            msg_body = old_msg['group_name'] + old_msg['ni_cheng'] + "\n" + old_msg['receive_time'] \
                       + "撤回了:" + "\n" + r"" + old_msg['msg_content']
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n链接是:" + old_msg.get('msg_share_url')
            itchat.send_msg(msg_body, toUserName='filehelper')
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            information.pop(old_msg_id)


# 短时间关闭程序后重连 hotReload
# 命令行显示二维码 enableCmdQR
itchat.auto_login(hotReload=True, enableCmdQR=1)
itchat.run()
