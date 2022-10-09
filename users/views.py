import datetime
import urllib.parse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .payfast import pfValidSignature, pfValidIP, pfValidPaymentData, pfValidServerConfirmation, generateSignature
from .serializers import *
from rest_framework.response import Response
from django.core.mail import send_mail
from heartflow import settings

from volunteers import models

passPhrase = 'jt7NOE43FZPn' #Maybe make this a secret code


# Create your views here.
@api_view(['GET', 'POST'])
@csrf_exempt
def insertTransaction(request):
    if request.method == 'POST':
        transaction = JSONParser().parse(request)
        transaction['status'] = 'IN_TRANSIT'
        transaction['address'] = 'TEMP_ADDRESS'

        transaction_serializer = transactionsSerializer(data=transaction)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return JsonResponse(transaction_serializer.data['payfastRef'], safe=False)
        else:
            print(transaction_serializer.errors)
            return HttpResponse(status=400)

@csrf_exempt
def online_coupons(request, status="", id=0):
    if request.method == 'GET':
        coupons = OnlineCoupons.objects.filter(status=status).filter(branch = request.user.branch)
        coupon_serializer = transactionsSerializer(coupons, many=True)
        return JsonResponse(coupon_serializer.data, safe=False)
    
    elif request.method == 'PATCH':
        coupon = OnlineCoupons.objects.get(id=id)
        coupon.status = status
        coupon.save()
        return HttpResponse(status=200)


@csrf_exempt
def cancelTransaction(request):
    if request.method == 'PATCH':
        transaction_ref = JSONParser().parse(request)
        print(transaction_ref)
        transaction = OnlineCoupons.objects.get(payfastRef=transaction_ref['payfastRef'])
        transaction.status = "TRANSACTION_CANCElED"
        transaction.save()
        return HttpResponse(status=200)


@csrf_exempt
def notificationPage(request):
    if request.method == 'POST':
        SANDBOX_MODE = True

        pfHost = 'sandbox.payfast.co.za' if SANDBOX_MODE else 'www.payfast.co.za'

        # Get posted variables from ITN and convert to a string
        pfData = {}
        postData = request.body.decode().split('&') # Make this more DJANGO friendly and better coding for now
        for i in range(0, len(postData)):
            splitData = postData[i].split('=')
            pfData[splitData[0]] = splitData[1]
        # and pfData[key] != '' and key != 'payment_status'
        pfParamString = ""
        m_payment_id = pfData['m_payment_id']
        transaction = OnlineCoupons.objects.get(payfastRef=m_payment_id)
        #
        if pfData['payment_status'] != 'COMPLETE':
            transaction.status = 'PAYMENT_FAILED'
            send_mail(
                subject= 'PAYMENT FAILED',
                message= 'Unfortunately your payment to Heartflow has failed',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[transaction.email]
            )
            transaction.save()
            return HttpResponse(status=200)

        for key in pfData:
            # Get all the data from PayFast and prepare parameter string  and pfData[key] != ''
            if key != 'signature':
                pfParamString += key + "=" + urllib.parse.quote_plus(pfData[key].replace("+", " ")) + "&"
        # After looping through, cut the last & or append your passphrase
        # payload += passPhrase
        # pfParamString = pfParamString[:-1]
        pfParamString += 'passphrase=' + passPhrase
        print(pfParamString)
        check1 = pfValidSignature(pfData, pfParamString)
        check2 = pfValidIP(request)
        check3 = pfValidPaymentData(transaction.paid, pfData)
        check4 = pfValidServerConfirmation(pfParamString, pfHost)
        print(check1)
        print(check2)
        print(check3)
        print(check4)

        if check2 and check3:
            # All checks have passed, the payment is successful
            transaction.status = 'PAYMENT_COMPLETE'
            send_mail(
                subject= 'PAYMENT COMPLETE',
                message= 'Your payment to Heartflow has been completed and will start being processed',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[transaction.email]
            )
           
            transaction.save()
        else:
            # Some checks have failed, check payment manually and log for investigation
            transaction.status = 'PAYMENT_AUTHENTICATION_ERRORS'
            transaction.save()
            send_mail(
                subject='PAYMENT ERROR',
                message='Unfortunately your payment to Heartflow has been compromised',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[transaction.email]
            )
            print("FAILED")
        return HttpResponse(status=200)


@csrf_exempt
def signature(request):
    if request.method == 'POST':
        pfData = JSONParser().parse(request)
        print(pfData)
        signature = generateSignature(pfData, passPhrase)
        return JsonResponse(signature, safe=False)

