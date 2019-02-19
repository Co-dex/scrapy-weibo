from cookiespool.scheduler import Scheduler
from cookiespool import importer


def main():
    while True:
        confirm = input("是否需要导入账号？（Y,n）")
        if confirm.lower() == 'y' or confirm.lower() == 'n':
            if confirm == 'y':
                confirm = True
                break
            else:
                confirm = False
                break
        print('input error！ try again...')

    if confirm:
        flag = input('是否自动扫描account.txt Y/N: ').lower()
        if flag == 'n':
            flag = False
        else:
            flag = True

        importer.main(auto_Scan=flag)
    else:
        s = Scheduler()
        s.run()


if __name__ == '__main__':
    main()
