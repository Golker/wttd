from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():  # form.is_valid internally calls form.full_clean()
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})
    # send email
    body = render_to_string('subscriptions/subscription_email.txt',
                            form.cleaned_data)

    mail.send_mail(subject='Confirmação de inscrição',
                   message=body,
                   from_email=settings.DEFAULT_FROM_EMAIL,
                   recipient_list=[form.cleaned_data['email']])

    Subscription.objects.create(**form.cleaned_data)

    # returns success feedback
    messages.success(request, 'Inscrição realizada com sucesso!')
    return HttpResponseRedirect('/inscricao/')


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


