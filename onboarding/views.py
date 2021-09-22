from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes, throttle_classes)
from rest_framework.response import Response

# Create your views here.
from onboarding.service import Service


class OTPViews(generics.ListAPIView):

    @staticmethod
    @api_view(['POST', ])
    def get_otp(request, *args, **kwargs):
        print(request.data)
        payload = request.data
        mobile = str(payload.get('mobile'))
        country_code = payload.get('country_code', '+91')

        if country_code in ['', None]:
            country_code = '+91'

        if country_code != '+91':
            return Response({
                'message': 'Currently we can verify only Indian Numbers!',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(mobile) != 10:
            return Response({
                'message': 'Please enter valid mobile number!',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)

        resp = Service().get_otp_for_user_mobile(mobile, country_code)
        return Response(resp, status=status.HTTP_200_OK)
