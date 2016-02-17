from django.contrib import admin
from .models import Question

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_on']
