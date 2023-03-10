# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, QueryDict
from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib import messages

from app.forms import CoinDataForm, CoinDataForm
from app.models import Transaction,CoinData
from app.utils import set_pagination


def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


class TransactionView(View):
    context = {'segment': 'transactions'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if request.GET.get("q"):
                return self.list(request) 
            elif pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            elif pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})
            
        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('transactions')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        transaction = self.get_object(pk)
        transaction.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Item deleted successfully')
            redirect_url = reverse('transactions')

        response = {'valid': 'success', 'message': 'Item deleted successfully', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        labels = []
        data = []

        ctx = {}
        url_parameter = request.GET.get("q")
        print("url_parameter", url_parameter)

        queryset = CoinData.objects.order_by('-created_at')
        for coin in queryset:
            labels.append(coin.coin_name)
            data.append(int(coin.price))
            filter_params = None

        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = Q(bill_for__icontains=key.strip())
                    else:
                        filter_params |= Q(bill_for__icontains=key.strip())

        transactions = CoinData.objects.order_by('-created_at')

        if url_parameter == '':
            transactions = CoinData.objects.order_by('-created_at')
            
        if url_parameter:
            transactions = CoinData.objects.filter(coin_name__icontains=url_parameter)
            # print(all_coins)
        else:
            transactions = CoinData.objects.order_by('-created_at')
        

        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if is_ajax_request:

            html = render_to_string(
                template_name="app/transactions/table.html", context={"transactions": transactions}
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        self.context["labels"] = labels
        self.context["data"] = data
        self.context['transactions'], self.context['info'] = set_pagination(request, transactions)
        if not self.context['transactions']:
            return False, self.context['info']

        return self.context, 'app/transactions/list.html'

    def edit(self, request, pk):
        transaction = self.get_object(pk)

        self.context['transaction'] = transaction
        self.context['form'] = CoinDataForm(instance=transaction)

        return self.context, 'app/transactions/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        transaction = self.get_object(pk)
        form = CoinDataForm(instance=transaction)
        context = {'instance': transaction, 'form': form}
        return render_to_string('app/transactions/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        transaction = get_object_or_404(CoinData, id=pk)
        return transaction

    def get_row_item(self, pk):
        transaction = self.get_object(pk)
        edit_row = render_to_string('app/transactions/edit_row.html', {'instance': transaction})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        transaction = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = CoinDataForm(form_data, instance=transaction)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'CoinData saved successfully')

            return True, 'CoinData saved successfully'

        if not is_urlencode:
            messages.warning(request, 'Error Occurred. Please try again.')
        return False, 'Error Occurred. Please try again.'
