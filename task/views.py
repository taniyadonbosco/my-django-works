# from os import uname
# import pwd
from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView,UpdateView
from task.models import Task
from task.forms import RegistrationForm,LoginForm,TaskUpdateform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
           return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



@method_decorator(signin_required,name="dispatch")

class IndexView(View):
    def get(self,request,*args,**kwargs):
         return render(request,"index.html")

class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"login.html")


class RegisterView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"register.html")


class AddTaskView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"add_task.html")

    def post(self,request,*args,**kwargs):
        name=request.user                             
        task=request.POST.get("task")
        Task.objects.create(user=name,task_name=task)
        messages.success(request,"task has been created")
        return redirect("signin")


@method_decorator(signin_required,name="dispatch")
class TaskListView(ListView):
    model=Task
    template_name="tasklist.html"
    context_object_name="todos"
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kwargs):
    #     if request.user.is_authenticated:
    #         qs=Task.objects.filter(user=request.user)
    #         return render(request,"tasklist.html",{"todos":qs})
    #     else:
    #         return redirect("signin")

       
@method_decorator(signin_required,name="dispatch")
class TaskDetailView(DetailView):
    model=Task
    template_name="taskdetail.html"
    context_object_name="todos"
    pk_url_kwarg="id"
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     task=Task.objects.get(id=id)
    #     return render(request,"taskdetail.html",{"todos":task})


@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Task.objects.filter(id=id).delete()
        messages.success(request,"task deleted")
        return redirect("todos-all")

class RegistrationView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register1.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"account created")
            return redirect("todo-all")
        else:
            messages.error(request,"registration failed")
            return render(request,"register1.html",{"form":form})
            

class LoginnView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login1.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("todo-all")
            else:
                messages.error(request,"invalid credentilals")
                return render(request,"login.html",{"form":form})

@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class TaskUpdateView(UpdateView):
    model=Task
    form_class=TaskUpdateform
    template_name="todo-update.html"
    pk_url_kwarg="id"
    success_url=reverse_lazy("todo-all")


    