from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, SESSION_KEY
from django.contrib.auth import login as auth_login
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, SignUpForm, LoginForm

import logging
logger = logging.getLogger(__name__)


def test(request, *args, **kwargs):
    return HttpResponse('OK')



def paginator(request, query_set, base_url, render_template):
    limit = 10

    try:
        page = int(request.GET.get('page', 1))     
    except ValueError:
        raise Http404

    paginator = Paginator(query_set, limit)     
    paginator.baseurl = base_url     
    page = paginator.page(page)
    return render(request, 
                  render_template, 
                  {'paginator': paginator, 
                   'page': page})



def new_questions(request, *args, **kwargs):
    return paginator(request,
                     Question.objects.new(),
                     '/?page=',
                     'qa/new_questions.html')
    


def popular_questions(request):
    return paginator(request,
                     Question.objects.popular(),
                     '/popular/?page=',
                     'qa/popular_questions.html')


def question_details(request, pk):
    question = get_object_or_404(Question, id=pk) 
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.clean()
            form.save(author=request.user)
            return HttpResponseRedirect(question.get_url())
    else:
        form = AnswerForm(initial={'question': pk})


    return render(request, 
                  'qa/question_details.html', 
                  {'question': question,
                   'answers': answers[:],
                   'form': form})


def question_add(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form.clean()
            new_question = form.save(author=request.user)
            return HttpResponseRedirect(new_question.get_url())
    else:
        form = AskForm()

    return render(request,
                  'qa/question_add.html',
                  {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.debug('new user created! %s', user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.debug('name / password: %s / %s', username, password)
            # user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('main_page'))
    else:
        form = SignUpForm()
        return render(request, 
                      'qa/signup.html', 
                      {'form': form})

# session cookie is not set on 10.42.153.224/login page
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.debug('authenticating name / password: %s / %s', username, password)
            user = authenticate(username=username, password=password)
            logger.debug('authenticated user %s', user)
            if user:
                auth_login(request, user)
                request.session.set_test_cookie()
                request.session['sessionid'] = request.session[SESSION_KEY]
            return HttpResponseRedirect(reverse('main_page'))
    else:
        form = LoginForm()
        return render(request, 
                      'qa/login.html', 
                      {'form': form})
