# import requests
# import easygui as gui
from cookiespool.db import RedisClient

conn = RedisClient('accounts', 'weibo')


def account_set(account, sep='----'):
    username, password = account.split(sep)
    result = conn.set(username, password)  # 导入数据库
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        account_set(account)


def scan_auto(filepath):
    print('开始自动录入...')
    with open(filepath, 'r', encoding='utf8') as f:
        while True:
            line = f.readline()
            if line:
                account_set(line)
                # print(line)
            else:
                break


def main(auto_Scan=True):
    """
    importer main(auto_Scan)
    :param auto_Scan: auto scan account.txt default is True
    :return: None
    """
    if auto_Scan:
        scan_auto('account.txt')
    else:
        scan()


if __name__ == '__main__':
    confirm = input('自动导入？(Y,n): ').lower()
    if confirm == 'n':
        main(auto_Scan=False)
        exit(0)
    main()
