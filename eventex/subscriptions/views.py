from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():  # internally calls form.full_clean()
            body = render_to_string('subscriptions/subscription_email.txt',
                                    form.cleaned_data)

            mail.send_mail(subject='Confirmação de inscrição',
                           message=body,
                           from_email='lucabezerra@gmail.com',
                           recipient_list=[form.cleaned_data['email'],
                                           'contato@eventex.com.br'])
            messages.success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)


