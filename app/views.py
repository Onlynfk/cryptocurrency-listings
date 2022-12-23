from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import CoinData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, JsonResponse



def home(request):
    ctx = {}
    url_parameter = request.GET.get("q")
    # print("url_parameter", url_parameter)

    labels = []
    data = []

    queryset = CoinData.objects.order_by('-price')[:5]
    for city in queryset:
        labels.append(city.coin_name)
        data.append(city.price)


    if url_parameter:
        all_coins = CoinData.objects.filter(coin_name__icontains=url_parameter)
        # print(all_coins)
    else:
        all_coins = CoinData.objects.order_by('-created_at')

   

    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if is_ajax_request:

        html = render_to_string(
            template_name="app/list.html", context={"coins": all_coins}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_coins, 8)
    try:
        coins = paginator.page(page)
    except PageNotAnInteger:
        coins = paginator.page(1)
    except EmptyPage:
        coins = paginator.page(paginator.num_pages)
    # logger.info(" process begins!")

    ctx["all"] = all_coins
    ctx["coins"] = coins
    ctx["labels"] = labels
    ctx["data"] = data
    
    return render(request, "app/index.html", context=ctx)

def coin(request, coinId):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        coin = get_object_or_404(CoinData, id=coinId)

        if request.method == 'DELETE':
            coin.delete()
            return JsonResponse({'status': 'Coin deleted!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
