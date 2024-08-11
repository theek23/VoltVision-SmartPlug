from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from user.models import User

@require_POST
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        try:
            unit = User.objects.get(email=email)
            return JsonResponse({'error': 'User already exists'}, status=409)

        except User.DoesNotExist:
            user = User(email=email, password=password)
            user.save()
            response_data = {
                'email': user.email,
                'password': user.password,
            }
            user_units = user.units.all()
            return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)

def get_user(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')

        if not email:
            return JsonResponse({'error': 'email parameter is required'}, status=400)

        try:
            user = User.objects.get(email=email)
            user_data = {
                'email': user.email,
                'password': user.password,
            }

            return JsonResponse(user_data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)

def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()

        units_list = list(users.values())

        return JsonResponse(units_list, safe=False)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=400)