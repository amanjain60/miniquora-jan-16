from django.conf.urls import url
from .views import all_questions, add_question
urlpatterns = [
    url(r'^all/$', all_questions),
    url(r'^add/$', add_question, name="add-question"),
]
