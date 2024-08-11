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
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from user.models import User


@require_POST
@csrf_exempt
def create_Unit(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        user = data.get('user')

        try:
            unit = Unit.objects.get(id=id)
            print(unit)
            return JsonResponse({'error': 'Unit already exists'}, status=409)

        except Unit.DoesNotExist:

            try:
                user_check = User.objects.get(email=user)

                place = data.get('place')
                unit = Unit(id=id, user=user_check, place=place)
                unit.save()
                response_data = {
                    'id': unit.id,
                    'user': user_check.email,
                    'place': place,
                }
                user_units = user_check.units.all()

                ###################################################
                csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv', f'{id}.csv')

                with open(csv_file_path, 'w', newline='') as csvfile:
                    fieldnames = ['time_date', 'watt']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    #writer.writerow({'time_date': unit.time_date, 'watt': unit.watt})

                    return JsonResponse(response_data)
            except Unit.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


@csrf_exempt
@require_GET
def get_All_unit(request):
    if request.method == 'GET':
        units = Unit.objects.all()

        units_list = list(units.values())

        return JsonResponse({'units': units_list}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


@csrf_exempt
@require_GET
def search_unit(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        user = data.get('user')
        try:
            unit = Unit.objects.get(user=user, id=id)
            response_data = {
                'id': unit.id,
                'user': unit.user.email,
                'place': unit.place,
            }
            return JsonResponse(response_data)
        except Unit.DoesNotExist:
            return JsonResponse({'error': 'Unit not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


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


def get_summery():
    # Example data
    voltage_readings = [220, 230, 225, 235, 240, 230, 220, 210, 225, 235, 240, 250]  # Voltage in volts
    current_readings = [5, 5.2, 5.1, 5.3, 5.5, 5.2, 5, 4.8, 5.1, 5.3, 5.5, 5.7]  # Current in amps
    timestamps = [
        datetime(2024, 6, 1, 0, 0), datetime(2024, 6, 1, 1, 0), datetime(2024, 6, 1, 2, 0), datetime(2024, 6, 1, 3, 0),
        datetime(2024, 6, 2, 0, 0), datetime(2024, 6, 2, 1, 0), datetime(2024, 6, 2, 2, 0), datetime(2024, 6, 2, 3, 0),
        datetime(2024, 6, 3, 0, 0), datetime(2024, 6, 3, 1, 0), datetime(2024, 6, 3, 2, 0), datetime(2024, 6, 3, 3, 0)
    ]  # Timestamps

    # Step 1: Calculate power in watts
    power_readings = [v * i for v, i in zip(voltage_readings, current_readings)]  # Power in watts

    # Step 2: Convert power readings to kWh (assuming hourly readings)
    power_kwh = [p / 1000 for p in power_readings]  # Convert to kWh

    # Step 3: Create a DataFrame for easier manipulation
    df = pd.DataFrame({
        'timestamp': timestamps,
        'power_kwh': power_kwh
    })

    # Set timestamp as index
    df.set_index('timestamp', inplace=True)

    # Step 4: Resample to daily consumption
    daily_consumption = df.resample('D').sum()

    # Step 5: Estimate average daily consumption
    avg_daily_consumption = daily_consumption['power_kwh'].mean()

    # Step 6: Predict total consumption for the rest of the month
    days_in_month = 30  # Assuming 30 days in the month
    days_passed = len(daily_consumption)
    days_remaining = days_in_month - days_passed

    estimated_total_consumption = avg_daily_consumption * days_in_month

    # Step 7: Apply utility rate to estimate the bill
    rate_per_kwh = 0.12  # Example rate in dollars per kWh
    estimated_bill = estimated_total_consumption * rate_per_kwh

    print(f"Daily consumption so far:\n{daily_consumption}")
    print(f"Average daily consumption: {avg_daily_consumption:.2f} kWh")
    print(f"Estimated total consumption for the month: {estimated_total_consumption:.2f} kWh")
    print(f"Estimated bill: ${estimated_bill:.2f}")

    # Optional: Visualize daily consumption
    plt.figure(figsize=(10, 6))
    plt.plot(daily_consumption.index, daily_consumption['power_kwh'], marker='o', linestyle='-',
             label='Daily Consumption (kWh)')
    plt.axhline(y=avg_daily_consumption, color='r', linestyle='--', label='Average Daily Consumption')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')
    plt.title('Daily Electricity Consumption')
    plt.legend()
    plt.grid(True)
    plt.show()


@require_POST
@csrf_exempt
def ex(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        return JsonResponse(data)


@csrf_exempt
@require_GET
def get_last_unit_id(request):
    try:
        last = Unit.objects.latest('id')
        next = int(last.id) + 1
        response = {'id': next}
    except Unit.DoesNotExist:
        response = {'id': 1}

    return JsonResponse(response)
