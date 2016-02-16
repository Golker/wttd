from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, Http404
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

    subscription = Subscription.objects.create(**form.cleaned_data)

    # send email
    body = render_to_string('subscriptions/subscription_email.txt',
                            {'subscription': subscription})

    mail.send_mail(subject='Confirmação de inscrição',
                   message=body,
                   from_email=settings.DEFAULT_FROM_EMAIL,
                   recipient_list=[subscription.email])

    return HttpResponseRedirect('/inscricao/1/')


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    context = {'subscription': subscription}
    return render(request, 'subscriptions/subscription_detail.html', context)


