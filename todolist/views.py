from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from todolist.models import Task_char 

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm   # how to create my own form
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    fields = ['username', 'password1', 'password2']
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task_char
    context_object_name = 'tasks'
    template_name = 'task_char_list.html'

    def get_context_data(self, **kwargs):
        # return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)    # super() обращается к родительскому классу (ListView)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            
        context['search_input'] = search_input

        # логика сортировки
        sort_by = self.request.GET.get('sort', 'updated_at')  # По умолчанию сортировка по дате создания
        order = self.request.GET.get('order', 'asc')  # По умолчанию порядок сортировки по возрастанию

        if order == 'desc':
            context['tasks'] = context['tasks'].order_by('completed', f'-{sort_by}')
        else:
            context['tasks'] = context['tasks'].order_by('completed', sort_by)
        
        context['sort_by'] = sort_by
        context['order'] = order
        
        return context
    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task_char
    context_object_name = 'task'
    template_name = 'task_char_detail.html'
    
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task_char
    fields = ['title', 'description', 'completed']
    # fields = '__all__'
    template_name = 'task_create.html'    # default *model*_from
    # form_class = TaskForm    # we can create our own form
    
    def get_success_url(self):
        # Получаем параметры из GET-запроса
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'updated_at')
        
        # Формируем URL с параметрами
        success_url = f"{reverse('tasks')}?order={order}&sort={sort_by}"
        return success_url
    
    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task_char.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            
        context['search_input'] = search_input

        # логика сортировки
        sort_by = self.request.GET.get('sort', 'updated_at')  # По умолчанию сортировка по дате создания
        order = self.request.GET.get('order', 'asc')  # По умолчанию порядок сортировки по возрастанию

        if order == 'desc':
            context['tasks'] = context['tasks'].order_by('completed', f'-{sort_by}')
        else:
            context['tasks'] = context['tasks'].order_by('completed', sort_by)
        
        context['sort_by'] = sort_by
        context['order'] = order
        
        return context
            

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task_char
    fields = ['title', 'description', 'completed']
    template_name = 'task_create.html'
    context_object_name = 'task'

    def get_success_url(self):
        # Получаем параметры из GET-запроса
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'updated_at')
        
        # Формируем URL с параметрами
        success_url = f"{reverse('tasks')}?order={order}&sort={sort_by}"
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task_char.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            
        context['search_input'] = search_input

        # логика сортировки
        sort_by = self.request.GET.get('sort', 'updated_at')  # По умолчанию сортировка по дате создания
        order = self.request.GET.get('order', 'asc')  # По умолчанию порядок сортировки по возрастанию

        if order == 'desc':
            context['tasks'] = context['tasks'].order_by('completed', f'-{sort_by}')
        else:
            context['tasks'] = context['tasks'].order_by('completed', sort_by)
        
        context['sort_by'] = sort_by
        context['order'] = order

        return context
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task_char
    context_object_name = 'del_task'
    template_name = 'task_char_confirm_delete.html'
    
    def get_success_url(self):
        # Получаем параметры из GET-запроса
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'updated_at')
        
        # Формируем URL с параметрами
        success_url = f"{reverse('tasks')}?order={order}&sort={sort_by}"
        return success_url
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task_char.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            
        context['search_input'] = search_input

        # логика сортировки
        sort_by = self.request.GET.get('sort', 'updated_at')  # По умолчанию сортировка по дате создания
        order = self.request.GET.get('order', 'asc')  # По умолчанию порядок сортировки по возрастанию

        if order == 'desc':
            context['tasks'] = context['tasks'].order_by('completed', f'-{sort_by}')
        else:
            context['tasks'] = context['tasks'].order_by('completed', sort_by)
        
        context['sort_by'] = sort_by
        context['order'] = order

        return context

    def delete(self, request, *args, **kwargs):
        # Удаляем объект
        self.object = self.get_object()
        self.object.delete()

        return HttpResponse(status=204)    

    
    
