import requests
from bs4 import BeautifulSoup as bs


import sys, os
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'studentInfo.settings'
import django
django.setup()


from showInfo.models import Course as course_model
from showInfo.models import StudentCourse as studentCourse_model
from showInfo.models import Student as student_model

xqh = 20171
main_url = "http://192.168.2.229/newkc/akcjj0.asp?xqh={}".format(xqh)
collega_url = "http://192.168.2.229/newkc/akechengdw.asp"
detail_url = "http://192.168.2.229/newkc/kccx.asp?flag=kkdw"
course_student_url = "http://192.168.2.229/newkc/kcxkrs.asp?ykch={}"
session = requests.session()
session.get(main_url)

question_student = []

class Course:
    def __init__(self, value):
        self.course_list = []
        self.value = value
    def post_info(self):
        data =  {
            'bh':self.value.encode('gb18030','ignore'),
            'SUBMIT':u'提交'
        }
        return data
    def get_content(self):
        response = session.post(detail_url, data=self.post_info())
        return response.content
    def save_course(self):
        soup = get_soup(self.get_content())
        t = soup.find_all('tr')
        for i in t[1:-3]:
            td = i.find_all('td')
            courseId = td[1].text.strip()
            courseName = td[2].text.strip()
            teacher = td[9].text.strip()
            time = td[11].text.strip()
            place = td[12].text.strip()
            self.course_list.append(courseId)
            course_model(course_id=courseId, course_name=courseName, time=time, place=place, teacher=teacher).save()
            # try:
            #     print ("courseId:{}, courseName:{}, teacher:{}, time:{}, place:{}".format(courseId, courseName, teacher, time, place))
            # except:
            #     print ("error")

class Student:
    def __init__(self, values):
        session.get(main_url)
        self.url = course_student_url.format(values)
        self.value = values
    def get_content(self):
        return get_html(self.url)
    def save_student(self):
        content = self.get_content()
        soup = get_soup(content)
        t = soup.find_all('tr')
        for i in t[3:]:
            stu_no = i.find_all('td')[1].text.strip()
            print (stu_no)
            try:
                studentCourse_model(student=student_model.objects.filter(stu_no=stu_no)[0], course=course_model.objects.get(course_id=self.value)).save()
            except:
                question_student.append(stu_no)


def get_html(url):
    response = session.get(url)
    return response.content

def get_soup(content):
    soup = bs(content,'html5lib')
    return soup

def get_option(soup):
    options = soup.find_all('option')
    values = []
    for option in options:
        values.append(option.text.strip())
    return values
if __name__ == "__main__":
    values = get_option(get_soup(get_html(collega_url)))
    for value in values:
        print (value)
        print ("-------------------------------------------")
        a = Course(value)
        a.save_course()
        for course in a.course_list:
            b = Student(course)
            print (course)
            print ("---------------")
            b.save_student()
