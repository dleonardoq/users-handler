from django.db import OperationalError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from users.models import Users
from users.serializer import UserSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def users(request, user_id=None):
    status_code = status.HTTP_200_OK
    user_data = {}
    if request.method == 'GET':
        if user_id and not user_id.isdigit():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'message': 'Id param must be an integer',
                'statusCode': status_code,
                'data': user_data
            }, status_code)
        if user_id:
            user_data, status_code = get_one(user_id=user_id)
        else:
            user_data, status_code = get_all()

    if request.method == 'POST':
        user_data, status_code = create(request)
    if request.method == 'PUT':
        user_data, status_code = update(request, user_id=user_id)
    if request.method == 'DELETE':
        user_data, status_code = delete(user_id=user_id)
    return Response(user_data, status_code)


def get_all():
    status_code = status.HTTP_200_OK

    users_data = Users.objects.filter(active=True)

    serializer = UserSerializer(users_data, many=True)

    if not users_data.exists():
        status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': 'Users not found',
            'statusCode': status_code,
            'data': {}
        }, status_code

    return {
        'message': 'OK',
        'statusCode': status_code,
        'data': serializer.data
    }, status_code


def get_one(user_id):
    status_code = status.HTTP_200_OK

    try:
        users_data = Users.objects.get(document_number=user_id, active=True)
    except Users.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': 'User not found',
            'statusCode': status_code,
            'data': {}
        }, status_code

    serialize = UserSerializer(users_data)

    return {
        'message': 'OK',
        'statusCode': status_code,
        'data': serialize.data
    }, status_code


def create(request):
    status_code = status.HTTP_201_CREATED

    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
        status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'Bad request',
            'statusCode': status_code,
            'data': serializer.errors
        }, status_code

    try:
        serializer.save()
    except OperationalError as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'message': 'Internal server error',
            'statusCode': status_code,
            'data': e
        }, status_code

    return {
        'message': 'User created',
        'statusCode': status_code,
        'data': serializer.data
    }, status_code


def update(request, user_id):
    status_code = status.HTTP_200_OK

    if not user_id:
        status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'Bad request',
            'statusCode': status_code,
            'data': 'Id param is needed'
        }, status_code

    try:
        user_data = Users.objects.get(document_number=user_id, active=True)
    except Users.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': 'User not found',
            'statusCode': status_code,
            'data': {}
        }, status_code

    new_user_data = request.data
    serializer = UserSerializer(user_data, data=new_user_data, partial=True)

    if not serializer.is_valid():
        status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'Bad request',
            'statusCode': status_code,
            'data': serializer.errors
        }, status_code

    try:
        serializer.save()
    except OperationalError as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'message': 'Internal server error',
            'statusCode': status_code,
            'data': e
        }, status_code

    return {
        'message': 'User updated',
        'statusCode': status_code,
        'data': serializer.data
    }, status_code


def delete(user_id):
    status_code = status.HTTP_200_OK

    if not user_id:
        status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'Bad request',
            'statusCode': status_code,
            'data': 'Id param is needed'
        }, status_code

    try:
        user_data = Users.objects.get(document_number=user_id, active=True)
    except Users.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': 'User not found',
            'statusCode': status_code,
            'data': {}
        }, status_code

    serializer = UserSerializer(
        user_data, data={'active': False}, partial=True)

    if not serializer.is_valid():
        status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'Bad request',
            'statusCode': status_code,
            'data': serializer.errors
        }, status_code

    try:
        serializer.save()
    except OperationalError as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'message': 'Internal server error',
            'statusCode': status_code,
            'data': e
        }, status_code

    return {
        'message': 'User deleted',
        'statusCode': status_code,
        'data': serializer.data
    }, status_code
