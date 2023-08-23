import markdown
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def mark(value):  # markdown 모듈과 mark_safe 함수를 이용하여 입력 문자열을 HTML로 변환하는 필터 함수
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions = extensions))