from django.shortcuts import render
import os
import csv
import tensorflow as tf
import pandas as pd
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from unit.models import Unit

@require_POST
@csrf_exempt
def create_Unit(request):
    data = json.loads(request.body.decode('utf-8'))
    id = data.get('id')
    time_date = data.get('time_date')
    watt = data.get('watt')
    unit = Unit(id=id, time_date=time_date, watt=watt)
    unit.save()
    response_data = {
        'id': unit.id,
        'time_date': unit.time_date,
        'watt': unit.watt,
    }

    ###################################################
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv', f'{id}.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['time_date', 'watt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'time_date': unit.time_date, 'watt': unit.watt})

    # return render(request, 'myapp/unit_list.html', {'units': all_unit})
    # Return the response as JSON
    return JsonResponse(response_data)


@csrf_exempt
@require_GET
def unit_details(request):
    data = json.loads(request.body.decode('utf-8'))
    id = data.get('id')

    if not id:
        return JsonResponse({'error': 'ID parameter is required'}, status=400)

    try:
        unit = Unit.objects.get(id=id)
        unit_data = detail(id)
        return JsonResponse(unit_data)
    except Unit.DoesNotExist:
        return JsonResponse({'error': 'Unit not found'}, status=404)


def detail(id):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv', f'{id}.csv')

    df = pd.read_csv(path)
    df

    df['time_date'] = pd.to_datetime(df['time_date'])

    dataset = tf.data.Dataset.from_tensor_slices((df['time_date'].astype(str).values, df['watt'].values))

    segments = []
    current_segment = []
    start_time = None
    response_data = {}

    for time, watt in dataset:
        time = time.numpy().decode()
        watt = watt.numpy()

        if watt == 0:
            if current_segment:
                segments.append(current_segment)
                current_segment = []
                start_time = None
        else:
            if not current_segment:
                start_time = time
            current_segment.append((time, watt))


    if current_segment:
        segments.append(current_segment)


    max_value = -float('inf')
    max_value_segment = None
    max_time_range = -float('inf')
    max_time_range_segment = None

    for segment in segments:
        segment_max_value = max(segment, key=lambda x: x[1])
        segment_time_range = (pd.to_datetime(segment[-1][0]) - pd.to_datetime(segment[0][0])).total_seconds()

        if segment_max_value[1] > max_value:
            max_value = segment_max_value[1]
            max_value_segment = segment

        if segment_time_range > max_time_range:
            max_time_range = segment_time_range
            max_time_range_segment = segment

    if max_value_segment:
        max_value_time_range = (max_value_segment[0][0], max_value_segment[-1][0])
        response_data['highest_value'] = float(max_value)
        response_data['time_range_of_highest_value_segment'] = {
            'start_time': max_value_time_range[0],
            'end_time': max_value_time_range[1]
        }

    if max_time_range_segment:
        max_time_range_times = (max_time_range_segment[0][0], max_time_range_segment[-1][0])
        response_data['highest_time_range'] = float(max_time_range)
        response_data['time_range_of_segment_with_highest_time_range'] = {
            'start_time': max_time_range_times[0],
            'end_time': max_time_range_times[1]
        }

        return response_data
