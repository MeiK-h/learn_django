from django import forms
from .models import Code
from django.core.exceptions import ValidationError


def file_type_valid(value):
    file_type_split = value.name.split('.')
    if len(file_type_split) < 2:
        raise ValidationError("你提交了个啥玩意连后缀名都没有")
    file_type = file_type_split[-1]
    if not file_type in Code.access_type:
        raise ValidationError("后缀名不合法")


class CodeForm(forms.Form):
    code = forms.FileField(validators=[file_type_valid])

