# coding=utf-8
import itchat

itchat.auto_login(hotReload=True, enableCmdQR=1)

friends = itchat.get_friends(update=True)

chatroom = '@1234567'
addroom = itchat.add_member_into_chatroom(chatroom, [friends[1]])
print(addroom)

if addroom['BaseResponse']['ErrMsg'] == '请求成功':
    status = addroom['MemberList'][0]['MemberStatus']
    itchat.delete_member_from_chatroom(chatroom['UserName'], [friends[1]])
    if status == 3:
        print('已经将你加入黑名单')
    elif status == 4:
        print('已经将你删除')
    else:
        print('仍是好友')
else:
    print('无法获取好友状态，预计已经达到接口调用限制')
