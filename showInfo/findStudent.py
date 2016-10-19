import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

import sys, os
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'studentInfo.settings'
import django
django.setup()

from showInfo.models import Student as showInfo_student
collega_url = 'http://192.168.2.20/axsxx/xy.ASP'
class_url = 'http://192.168.2.20/axsxx/xy1.asp'
detail_url = 'http://192.168.2.20/axsxx/xy2.asp'

class Collega:
    def __init__(self,value):
        self.value = value
        self.class_list = [];
    def post_info(self):
        data =  {
        'bh':self.value,
        'SUBMIT':u'提交'
        }
        for key in data.keys():
            data[key] = data[key].encode('gb18030','ignore')
        data = urllib.parse.urlencode(data)
        return data.encode('gb18030','ignore')
    def get_content(self):
        req = urllib.request.Request(class_url,self.post_info())
        response = urllib.request.urlopen(req)
        return response.read().decode('gb18030')
    def get_class(self):
        content = self.get_content()
        self.class_list = get_option(get_soup(content))
        return self.class_list

class SzuClass:
    def __init__(self,value,collega):
        self.value = value
        self.collega = collega
        self.student_list = []
    def post_info(self):
        data =  {
        'bh':self.value,
        'SUBMIT':u'提交'
        }
        for key in data.keys():
            data[key] = data[key].encode('gb18030','ignore')
        data = urllib.parse.urlencode(data)
        return data.encode('gb18030','ignore')
    def get_content(self):
        req = urllib.request.Request(detail_url,self.post_info())
        response = urllib.request.urlopen(req)
        return response.read().decode('gb18030')
    def get_student(self):
        soup = get_soup(self.get_content())
        tr_list = soup.find_all('tr')
        for num in range(1,len(tr_list)-1):
            stu_td = tr_list[num].find_all('td')
            each_student = Student(stu_td[1].text,stu_td[2].text,stu_td[3].text,stu_td[4].text,stu_td[5].text,self.value)
            self.student_list.append(each_student)
        return self.student_list


class Student:
    def __init__(self,stu_no,name,gender,profess,collega,className):
        self.stu_no = stu_no
        self.name = name
        self.gender = gender
        self.profess = profess
        self.collega = collega
        self.className = className
    def toSQL(self):
        '''
        name = models.CharField(max_length=100)
        gender = models.CharField(max_length=10)
        stu_no = models.CharField(max_length=50)
        profess = models.CharField(max_length=100)
        collega = models.CharField(max_length=100)
        className = models.CharField(max_length=100)
        :return:
        '''
        print (self.stu_no)
        showInfo_student(name=self.name.strip(),gender=self.gender.strip(),stu_no=self.stu_no.strip(),profess=self.profess.strip(),collega=self.collega.strip(),className=self.className.strip()).save()



def get_html(url):
    response = urllib.request.urlopen(url)
    content = response.read()
    content = content.decode('gb18030')
    return content
def get_soup(content):
    soup = BeautifulSoup(content,'html5lib')
    return soup

def get_option(soup):
    options = soup.find_all('option')
    values = []
    for option in options:
        values.append(option.text.strip())
    return values

if __name__ == '__main__':
    values = get_option(get_soup(get_html(collega_url)))
    for value in values:
        each_collega = Collega(value)
        class_list = each_collega.get_class()
        for each_class in class_list:
            a = SzuClass(each_class,value)
            student_list = a.get_student()
            for each_student in student_list:
                each_student.toSQL()
            

