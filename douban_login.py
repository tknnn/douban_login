#encoding:utf-8
import requests
from HTMLParser import HTMLParser
from PIL import Image
import random

class DoubanClient(object):
    def __init__(self):
        headers = {
            'User - Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36',
            'origin': 'http://www.douban.com'
        }
        self.session = requests.session()
        self.session.headers.update(headers)

    def login(self, username, password, source="index_nav",
              redir="http://www.douban.com/",
              login='登录'):
        url = 'https://accounts.douban.com/login'
        r = self.session.get(url)
        (captcha_id, captcha_url) = _get_captcha(r.content)
        if captcha_id: #有验证码
            r = self.session.get(captcha_url)
            with open('captcha.jpg','wb') as f:
                f.write(r.content)
            try:
                im = Image.open('captcha.jpg') #手动识别  自动识别需要用到一个库
                im.show()
                im.close()
            except:
                pass
            captcha_solution = raw_input('please input solution for captcha: ')
            post_data = {
                'source':source,
                'redir':redir,
                'form_email':username,
                'form_password':password,
                'captcha-solution':captcha_solution,
                'captcha-id':captcha_id,
                'login':login
            }
        else:
            post_data = {
                'source': source,
                'redir': redir,
                'form_email': username,
                'form_password': password,
                'login': login
            }
        headers = {
            'referer': 'https://accounts.douban.com/login?redir=https://www.douban.com/&source=index_nav',
            'host': 'accounts.douban.com'
        }
        print post_data
        self.session.post(url, data=post_data, headers=headers)
        print self.session.cookies.items()

    def send_comment(self):
        base_url = 'https://www.douban.com/group/topic/106286806/'
        send_url = 'https://www.douban.com/group/topic/106286806/add_comment'
        content = self.session.get(base_url).content
        ck = _get_ck(content)
        comment = random.choice([u'有人在看吗',u'有人吗'])
        send_data = {
            'ck': ck,
            'rv_comment':comment,
            'start':'0',
        }
        try:
            self.session.post(send_url, data=send_data)
            print u'评论成功'
        except:
            print u'评论失败'

    # def edit_signature(self, username, signature):
    #     url = 'https://douban.com/people/%s/' %username
    #     r = self.session.get(url)
    #     print r.text
    #     data = {
    #         'ck': _get_ck(r.content),
    #         'signature': signature
    #     }
    #     url = 'https://www.douban.com/j/people/%s/edit_signature' %username
    #     headers = {
    #         'referer':url,
    #         'host':'www.douban.com',
    #         'x-requested-with':'XMLHttpRequest'
    #     }
    #     r = self.session.post(url,data=data,headers=headers)
    #     print r.content

def _get_captcha(content): #获取验证码的id和url
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self) #初始化
            self.captcha_id = None
            self.captcha_url = None

        def handle_starttag(self, tag, attrs): #tag是标签 attrs是属性
            if tag == 'img' and _attr(attrs, 'id') == 'captcha_image' and _attr(attrs,'class')=='captcha_image':
                self.captcha_url = _attr(attrs,'src')

            if tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
                self.captcha_id = _attr(attrs, 'value')

    p = CaptchaParser()
    p.feed(content) #把需要解析的数据传给feed方法解析
    return p.captcha_id, p.captcha_url

def _attr(attrs, attrname): #attrs是所有的属性， attrname是一个属性
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None

def _get_ck(content):#修改签名
    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck=None
        def handle_starttag(self, tag, attrs):
            if tag == 'input' and _attr(attrs, 'type') == 'value':
                self.ck = _attr(attrs, 'value')

if __name__ == '__main__':
    username = raw_input('username: ')
    password = raw_input('password: ')
    #password = get_pass.get_pass('password: ')
    d = DoubanClient()
    d.login(username, password)
    while True:
        d.send_comment()
        mm = raw_input('请输入命令 1.继续 2.退出')
        if mm == '2':
            break



