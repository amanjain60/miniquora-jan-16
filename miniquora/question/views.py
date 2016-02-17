from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Question


# Create your views here.
@csrf_exempt
def all_questions(request):
    context = {'q_list' : Question.objects.all() }
    return render(request, 'question/index.html', context);

@require_GET
def show_question_add_form(request):
    return render(request, 'question/create_form.html');

@require_POST
def save_question(request):
    title = request.POST.get('title' , '')
    if not title:
        raise Http404
    q = Question.objects.create(title = title, created_by = request.user);
    return HttpResponse('ok');

@require_GET
def get_question(request, id = None):
    if not id:
        raise Http404;
    q = get_object_or_404(Question, id=id);
    data = serializers.serialize('json', [q]);
    return HttpResponse(data, content_type = "application/json");

    


