from django.urls import path
from .views import formula_editor, comparator

urlpatterns = [
    path('', formula_editor, name='formula_editor'),
    path('comparator/', comparator, name='comparator'),
]