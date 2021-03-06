#coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from showInfo.models import Student, Course, StudentCourse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
class index(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        choice = request.POST.get('choice')
        value = request.POST.get('value')
        if(choice=='1'):
            result = Student.objects.filter(name=value)
            return render(request, 'result.html',{'result_list':result})
        else:
            result = Student.objects.get(stu_no=value)
            return render(request, 'result.html',{'result_list':[result]})

class course(View):
    def get(self, requests):
        stu_no = requests.GET.get('stu_no')
        try:
            s = Student.objects.filter(stu_no=stu_no)[0]
            course = []
            studentcourse = StudentCourse.objects.filter(student=s)
            '''
                course:
                   course_name: xxxx
                   course_time: []
                   course_place: []
            '''
            for c in studentcourse:
                course_name = c.course.course_name
                t = c.course.time.split(";")
                p = c.course.place.split(";")
                course_time = []
                course_place = []
                for index in range(len(t)):
                    limit = t[index][0]
                    if t[index] == ".":
                        continue
                    if p[index] == u"实验（学院自行安排实验室）":
                        p[index] = u"实验室"
                    if limit == u"单":
                        day = translateDay(t[index][1:3])
                        time = translateTime(t[index][3:])
                        course_time.append(str(day)+"_"+str(time)+"_"+"1")
                        course_place.append(p[index])
                    elif limit == u"双":
                        day = translateDay(t[index][1:3])
                        time = translateTime(t[index][3:])
                        course_time.append(str(day) + "_" + str(time) + "_" + "2")
                        course_place.append(p[index])
                    else:
                        day = translateDay(t[index][0:2])
                        time = translateTime(t[index][2:])
                        course_time.append(str(day) + "_" + str(time) + "_" + "1")
                        course_place.append(p[index])
                        course_time.append(str(day) + "_" + str(time) + "_" + "2")
                        course_place.append(p[index])
                course.append({
                    'course_name': course_name,
                    'course_time': course_time,
                    'course_place': course_place
                })
        except (Exception):
            data = {
                'status': 'error',
                'stu_name': 'null',
                'course': []
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        data = {
            'status': 'success',
            'stu_name': s.name,
            'course': course
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def student_interface(request):
    if request.method == "POST":
        choice = request.POST.get('choice')
        value = request.POST.get('value')
        if (choice == '1'):
            result = Student.objects.filter(name=value)
            s = [{'stu_no': i.stu_no, 'stu_name': i.name, 'gender': i.gender, 'collega': i.collega, 'profess': i.profess, 'class': i.className} for i in result]
            status = 'success'
            if len(s) == 0:
                status = 'empty'
            data = {
                'status': status,
                'count': len(s),
                'student': s
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            result = Student.objects.filter(stu_no=value)
            s = [
                {'stu_no': i.stu_no, 'stu_name': i.name, 'gender': i.gender, 'collega': i.collega, 'profess': i.profess,
                 'class': i.className} for i in result]
            status = 'success'
            if len(s) == 0:
                status = 'empty'
            data = {
                'status': status,
                'count': len(s),
                'student': s
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse("emmmm")

def translateDay(day):
    return {
        u'周一': 1,
        u'周二': 2,
        u'周三': 3,
        u'周四': 4,
        u'周五': 5
    }[day]

def translateTime(time):
    return {
        '1,2': 1,
        '3,4': 2,
        '5,6': 3,
        '7,8': 4,
        '9,10': 5,
        '11,12': 6
    }[time]