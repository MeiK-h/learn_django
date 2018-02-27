import os

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import CodeForm
from .models import Checker, Code, Jplag


class IndexView(generic.ListView):
    template_name = 'jplag/index.html'
    context_object_name = 'checker_list'

    def get_queryset(self):
        return Checker.objects.filter()


class CheckerView(generic.DeleteView):
    model = Checker
    template_name = 'jplag/checker.html'

    def get_queryset(self):
        return Checker.objects.all()


def new_checker(request):
    if not request.user.is_authenticated:
        return render(request, 'jplag/error.html', {'error_message': '您未登录'})
    checker = Checker(user=request.user,
                      title='new checker - ' + request.user.username)
    checker.save()
    return HttpResponseRedirect(reverse('jplag:index'))


def upload_code(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'jplag/error.html', {'error_message': '您未登录'})
    if request.method != 'POST':
        form = CodeForm()
    else:
        form = CodeForm(request.POST, request.FILES)
        if form.is_valid():
            checker = Checker.objects.get(id=pk)
            code = Code(code=form.cleaned_data['code'], checker=checker)
            code.save()
            return HttpResponseRedirect(reverse('jplag:checker', args=(checker.id,)))
    return render(request, 'jplag/upload_code.html', {'form': form})


def delete_code(request, pk1, pk2):
    if not request.user.is_authenticated:
        return render(request, 'jplag/error.html', {'error_message': '您未登录'})
    code = Code.objects.get(id=pk2)
    if os.path.exists(code.code.path):
        os.remove(code.code.path)
    code.delete()
    return HttpResponseRedirect(reverse('jplag:checker', args=(pk1, )))


def run_jplag(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'jplag/error.html', {'error_message': '您未登录'})
    checker = Checker.objects.get(id=pk)
    codes = Code.objects.filter(checker=checker).all()
    jplag = Jplag(pk)
    for code in codes:
        jplag.copy_file_to_jplag_tmp(code.code.path)
    language = request.GET.get('language', 'c/c++')
    jplag.make_run_cmd(language=language)
    rst = jplag.run()
    return render(request, 'jplag/run_jplag.html', {'rst': rst, 'result_url': '/uploads/result/{}/index.html'.format(checker.id)})
