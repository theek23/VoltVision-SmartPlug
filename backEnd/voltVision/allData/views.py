from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from allData.models import AllData


@require_POST
@csrf_exempt
def add(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        unit_id = data.get('id')
        time = data.get('time')
        volt = data.get('volt')
        amp = data.get('amp')

        allData = AllData(unit_id=unit_id, time_date=time, volt=volt, amp=amp)
        allData.save()

        return JsonResponse({'ok': 'added'}, status=200)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)
