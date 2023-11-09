from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserReg(request.POST)
        form2 = UserProf(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            pr = form.save(commit=False)
            pr.is_active = False
            pr.save()
            username = form.cleaned_data.get('username')
            profile = form2.save(commit=False)

            current_user = User.objects.get(username=username)

            profile.user = current_user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': pr,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(pr.pk)),
                'token': account_activation_token.make_token(pr),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = UserReg()
        form2 = UserProf()
    return render(request, 'register.html', {'form': form, 'form2': form2})