from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from src.base.models import RegistryModel
from src.base.serializers import CallerIdSerializer


@csrf_exempt
def view_call_id(request):
    context = {'phone': ''}

    if request.method == "POST":
        phone = request.POST.get('phone')
        data = RegistryModel.objects.get_data_about_phone(phone=phone)
        if data:
            data = CallerIdSerializer(data, many=False).data
            context = {'phone': request.POST.get('phone'), 'data': data}

        render(request, 'result_caller_id.html', context)
    return render(request, 'result_caller_id.html', context)
