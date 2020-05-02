from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from model import Question, Answer


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
    return paginator(request
                     Question.objects.popular(),
                     '/popular/?page=',
                     'qa/popular_questions.html')

def question_details(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Post.DoesNotExist:         
        raise Http404     

    return render(request, 
                  'question_details.html', 
                  {'question': question,
                   'answers': Answer.objects.filter(question=question)[:]})

