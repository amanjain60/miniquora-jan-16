from django.conf.urls import url
from .views import all_questions, get_question, show_question_add_form, save_question
urlpatterns = [
    url(r'^all/$', all_questions),
    url(r'^(?P<id>[0-9]+)/$', get_question),
    url(r'^add/$', show_question_add_form),
    url(r'^save/$', save_question),
]
