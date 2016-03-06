from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Question
from .forms import QuestionCreateForm


# Create your views here.
@csrf_exempt
def all_questions(request):
    context = {'q_list' : Question.objects.all() }
    return render(request, 'question/index.html', context);

@require_http_methods(['GET', 'POST'])
@login_required
def add_question(request):
    if request.method == 'GET':
        f = QuestionCreateForm(initial={'title': 'Hey!'})
    else:
        f = QuestionCreateForm(request.POST)
        if f.is_valid():
            question_obj = f.save(commit = False)
            question_obj.created_by = request.user
            question_obj.save()
            return HttpResponse('ok')
    return render(request, 'question/add.html', {'f': f})
