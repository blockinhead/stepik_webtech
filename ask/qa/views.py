from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm


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
            form.save()
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
            new_question = form.save()
            return HttpResponseRedirect(new_question.get_url())
    else:
        form = AskForm()

    return render(request,
                  'qa/question_add.html',
                  {'form': form})
