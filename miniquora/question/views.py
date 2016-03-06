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
        f = QuestionCreateForm()
    else:
        f = QuestionCreateForm(request.POST)
        if f.is_valid():
            question_obj = f.save(commit = False)
            question_obj.created_by = request.user
            question_obj.save()
            return HttpResponse('ok')
    return render(request, 'question/add.html', {'f': f})

@require_http_methods(['GET', 'POST'])
@login_required
def edit_question(request, id = None):
    question_obj = get_object_or_404(Question, id = id)
    if question_obj.created_by != request.user:
        raise Http404()
    if request.method == 'GET':
        f = QuestionCreateForm(instance = question_obj)
    else:
        f = QuestionCreateForm(request.POST, instance = question_obj)
        if f.is_valid():
            question_obj = f.save()
            return HttpResponse('ok')
    context = { 'f' : f, 'q_id': question_obj.id }
    return render(request, 'question/edit.html', context)
