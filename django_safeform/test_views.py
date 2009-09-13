from django.conf.urls.defaults import patterns
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django_safeform import SafeForm, csrf_protect, csrf_utils

class BasicForm(forms.Form):
    name = forms.CharField(max_length = 100)
SafeBasicForm = SafeForm(BasicForm)

@csrf_protect
def safe_form_view(request):
    form = SafeBasicForm(request)
    if form.is_valid():
        return HttpResponse(
            'Valid: %s' % form.cleaned_data['name']
        )
    return HttpResponse("""
        <form action="." method="post">
        %s
        <p><input type="submit"></p>
        </form>
    """ % form.as_p())

@csrf_protect
def hand_rolled(request):
    if request.method == 'POST':
        csrf_token = request.POST.get('csrf_token', '')
        if not csrf_utils.validate_csrf_token(csrf_token, request):
            return HttpResponse('Invalid CSRF token')
        else:
            return HttpResponse('OK')
    else:
        return HttpResponse("""
        <form action="." method="post">
        <input type="text" name="name">
        <input type="hidden" name="csrf_token" value="%s">
        </form>
        """ % csrf_utils.new_csrf_token(request))

urlpatterns = patterns('',
    (r'^safe-basic-form/$', safe_form_view),
    (r'^hand-rolled/$', hand_rolled),
)
