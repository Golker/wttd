from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():  # form.is_valid internally calls form.full_clean()
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    subscription = form.save()

    # send email
    body = render_to_string('subscriptions/subscription_email.txt',
                            {'subscription': subscription})

    mail.send_mail(subject='Confirmação de inscrição',
                   message=body,
                   from_email=settings.DEFAULT_FROM_EMAIL,
                   recipient_list=[subscription.email])

    return HttpResponseRedirect(r('subscriptions:detail', subscription.pk))


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    context = {'subscription': subscription}
    return render(request, 'subscriptions/subscription_detail.html', context)


