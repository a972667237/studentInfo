from django.shortcuts import render
from django.views.generic import View
from showInfo.models import Student
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
