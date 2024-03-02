import time

import requests
import re
from concurrent.futures import ThreadPoolExecutor


class Euorg:
    def __init__(self):
        self.http = requests.Session()
        self.have_session()

    def have_session(self):
        """初始化，获取 cookie 等等"""
        res = self.http.get('https://nic.eu.org/arf/en/contact/bydom', timeout=30)
        text = res.text
        self.csrf = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="(\S+?)">', text).group(1)

    def scan(self, domain):
        """扫描单域名，已注册返回用户名，未注册返回 None"""
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://nic.eu.org/arf/en/contact/bydom'
        }

        data = {
            'domain': domain,
            'change': 'Find contacts for this domain',
            'csrfmiddlewaretoken': self.csrf
        }

        text = self.http.post('https://nic.eu.org/arf/en/contact/bydom', timeout=30, headers=headers, data=data).text

        re_user = re.search(r'My handle is (\S+?)-FREE', text)
        if re_user is None:
            return None
        else:
            return re_user.group(1)


def write_regist(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    example = Euorg()
    pool = ThreadPoolExecutor(max_workers=8)

    # 读取字典
    f = open('./zidian.txt')
    domain = f.read().splitlines()
    f.close()
    domains = [i + '.eu.org' for i in domain]

    # 记录结果
    results = pool.map(example.scan, domains)
    # 代表数组下标
    flag = 0

    # 未注册
    noregist = []
    # 已注册
    regist = []
    # 总长度
    sumlength = len(domain)
    # 打印结果
    for i in results:
        print(f'{(flag + 1) / sumlength:.2%} : {flag + 1} / {sumlength} >>> {domains[flag]}\t', i)
        if i is None:
            noregist.append(domains[flag] + '.eu.org')
        else:
            regist.append(domains[flag] + '.eu.org' + '\t' + i)
        flag = flag + 1

    write_regist('./regist.txt', '\n'.join(regist))
    write_regist('./noregist.txt', '\n'.join(noregist))


if __name__ == '__main__':
    print('作者：勿埋我心')
    print('作者博客: https://www.SkyQian.com')
    print('源码: https://github.com/WuSuoV/ScanDomainEuorg \n')
    print('>>> 开始运行~')
    # 计算时间
    start_time = time.time()
    main()
    now_time = time.time()

    print(f'\n>>> 运行结束，共耗时 {now_time - start_time:.2f} 秒。所得运行结果，在当前所在目录下，请查收。\n')
    input('>>> 按任意键退出……')
