from CookiesPool.cookiespool.scheduler import Scheduler
from CookiesPool.cookiespool import importer


def main():
    while True:
        confirm = input("是否需要导入账号？（Y,n）")
        if confirm.lower() == 'y' or confirm.lower() == 'n':
            if confirm == 'y':
                confirm = True
            else:
                confirm = False
            break
        print('input error！ try again...')

    if confirm:
        auto_flag = False if input('是否自动扫描account.txt Y/N: ').lower() == 'n' else auto_flag = True
        importer.main(auto_Scan=auto_flag)
    else:
        s = Scheduler()
        s.run()


if __name__ == '__main__':
    main()
