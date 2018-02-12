import os
import platform
import re
import requests
from bs4 import BeautifulSoup


class GetWallPaper(object):
    def __init__(self, pages):
        self.headers = {
            'Connection': 'Keep-Alive',
            'Content-Type': 'text.html; charset-UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        self.url = 'https://wallpapershome.com'
        self.getPages = pages

    def analysis_url(self, *args):
        self.mkdir()
        if self.getPages:
            startpage = self.getPages[0]
            endpage = self.getPages[1]
            print('抓取第%s页到%s页的壁纸' % (startpage, endpage))
            for index, page in enumerate(range(startpage, endpage)):
                print('开始抓取第%s页的壁纸' % str(index+1))
                url = '?page=' + str(page)
                try:
                    html_content = self.request(url, args[0])
                    href_list = BeautifulSoup(html_content.text, 'lxml').find('div', class_='pics', id='pics-list').find_all('a')
                except Exception as err:
                    print('获取抓取网页的内容出错', err)
                else:
                    self.get_img(href_list)
        else:
            html_content = self.request('')
            href_list = BeautifulSoup(html_content.text, 'lxml').find('div', class_='pics', id='pics-list').find_all('a')
            self.get_img(href_list)

    def get_img(self, href_list):
        for idx, a in enumerate(href_list):
            print('正在获取第%s张壁纸' % str(idx+1))
            img_html_href = a['href']
            try:
                img_html_content = self.request(img_html_href)
                img_real_a = BeautifulSoup(img_html_content.text, 'lxml').find('div', id='res-list').find(href=re.compile('3840x2160'))
                # print(BeautifulSoup(img_html_content.text, 'lxml').find('div', id='res-list'))
            except Exception as err:
                print('获取大图网页内容出错', err)
            else:
                img_real_href = img_real_a['href']
                self.save(img_real_href, str(idx + 1))

    def save(self, img_url, idx):

        img_name = img_url[img_url.rfind('/')+1:]
        print('正在保存壁纸[%s]' % img_name)
        f = open(img_name, 'ab')
        try:
            img = self.request(img_url)
            f.write(img.content)
            f.close()
        except Exception as err:
            print('保存图片失败', err)
        else:
            print('第%s壁纸下载完成' % idx)

    def analysis_platform(self):
        if platform.system() == 'Darwin':
            return '/Users/qiandaxian/Pictures/'
        else:
            return 'd:/'

    def mkdir(self):
        temp_dir_name = 'temp_wallpapers'
        path = self.analysis_platform()
        temp_dir = path + temp_dir_name
        is_exsist = os.path.exists(temp_dir)
        if not is_exsist:
            os.makedirs(temp_dir)
            print('在%s目录下创建一个壁纸文件夹[%s]' % (temp_dir, temp_dir_name))
        os.chdir(temp_dir)
        print('切换至目录%s保存壁纸' % temp_dir)

    def request(self, second_url, *cat):
        if cat:
            full_url = self.url + '/' + cat[0] + '/' + second_url
        else:
            full_url = self.url + second_url
        try:
            content = requests.get(full_url, headers=self.headers, timeout=30)
            return content
        except requests.exceptions.ConnectTimeout:
            print('连接超时')
        except requests.exceptions.ConnectionError:
            print('连接错误')


# nature 自然
paper = GetWallPaper([1, 10])
paper.analysis_url('nature')