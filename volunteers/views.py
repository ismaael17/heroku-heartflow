import mimetypes
from pathlib import Path
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from .customToken import decode_reset_token, encoded_reset_token
from django.core import mail

from .models import *
from .models import discardLost as discardLostModel
from .serializers import *
from users.models import *

from users.serializers import *

from django.core.mail import EmailMultiAlternatives
from heartflow.settings import BASE_DIR
import os.path
import re

from email.mime.base import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart


@api_view(['GET', 'POST'])
@csrf_exempt
def volunteersCRUD(request):
    if request.method == 'POST':
        volunteer_data = JSONParser().parse(request)
        if Volunteers.objects.filter(email=volunteer_data['email']).exists():
            return HttpResponse(status=409)
        else:
            volunteer_data['password'] = make_password("password")
            serializer = volunteerSerializer(data=volunteer_data)
            print(volunteer_data['branch'])
            try:
                thisbranch = branch.objects.get(name=volunteer_data['branch'])
            except:
                return HttpResponse(status=400)

            branchString = volunteer_data['branch']
            volunteer_data['branch'] = thisbranch.id
            if serializer.is_valid():
                volunteer = serializer.save()
                token = Token.objects.get(user=volunteer).key
                volunteer_data['Token'] = token
                send_mail(
                    subject='New volunteer request from ' + volunteer_data['first_name'] + ' ' + volunteer_data[
                        'last_name'],
                    message='New volunteer request from ' + volunteer_data['first_name'] + ' ' + volunteer_data[
                        'last_name'] + '\n' + 'Email: ' + volunteer_data['email'] + '\n' + 'Branch: ' + branchString,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )
                return Response(volunteer_data, status=200)

            print(serializer.errors)
            return HttpResponse(status=400)


class volunteerInfo(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request, id = 0):
        if (id == 0):
            volunteer = request.user
            serializer = volunteerSerializer(volunteer)
        else:
            volunteer = Volunteers.objects.get(id=id)
            serializer = volunteerSerializer(volunteer)
        return Response(serializer.data, status=200)

    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def patch(self, request):
        volunteer = request.user
        volunteer_data = JSONParser().parse(request)
        serializer = volunteerSerializer(volunteer, data=volunteer_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class volunteerExchangeInfo(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request):
        volunteer = request.user
        volunteers = Volunteers.objects.filter(branch=volunteer.branch).exclude(id=volunteer.id)
        serializer = volunteerSerializer(volunteers, many=True)
        return Response(serializer.data, status=200)



class pendingVolunteer(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def patch(self, request, status=""):
        if request.method == 'PATCH':
            if status == "approve":
                volunteer_data = JSONParser().parse(request)
                volunteer = Volunteers.objects.get(id=volunteer_data['id'])

                volunteer.status = "approve"
                token = encoded_reset_token(volunteer.id)
                link = 'http://' + 'localhost:3000' + '/setpassword/' + "?token=" + token
                html_context = {'url': link}
                msg = EmailMultiRelated('Volunteer Request Approved!', 'Plain text version', 'Heartflow',
                                        [volunteer.email])

                htmly = get_template(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/approved.html'))
                html = htmly.render(html_context)

                msg.attach_alternative(html, 'text/html')

                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img6.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img5.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img4.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img3.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img2.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img1.png'))

                msg.send()

                volunteer.save()
                # send email to volunteer with link to set password
                return HttpResponse(status=200)

            elif status == "reject":
                volunteer_data = JSONParser().parse(request)
                volunteer = Volunteers.objects.get(id=volunteer_data['id'])

                volunteer.status = "reject"

                htmly = get_template(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/rejected.html'))
                html_context = {'url': 'https://heartflow.org.za/contact-us/'}
                html = htmly.render(html_context)

                msg = EmailMultiRelated('Volunteer Request Rejected', 'Plain text version', 'Heartflow',
                                        [volunteer.email])

                msg.attach_alternative(html, 'text/html')

                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img6.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img5.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img4.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img3.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img2.png'))
                msg.attach_related_file(os.path.join(BASE_DIR, 'volunteers/templates/email/approved/images/img1.png'))

                msg.send()

                volunteer.save()
                # send email to volunteer with link to set password
                return HttpResponse(status=200)

            elif status == "meeting_scheduled":
                volunteer_data = JSONParser().parse(request)
                volunteer = Volunteers.objects.get(id=volunteer_data['id'])
                volunteer.status = "meeting_scheduled"
                volunteer.save()
                send_mail(
                    subject='Meeting Scheduled',
                    message='Your meeting has been scheduled for ' + volunteer_data['date'] + '.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )

                return HttpResponse(status=200)

            elif status == "pending_review":
                volunteer_data = JSONParser().parse(request)
                volunteer = Volunteers.objects.get(id=volunteer_data['id'])
                volunteer.status = "pending_review"
                volunteer.save()
                send_mail(
                    subject='Pending Review',
                    message='Your application is pending review',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )

            elif status == 'inactive':
                volunteer_data = JSONParser().parse(request)
                volunteer = Volunteers.objects.get(id=volunteer_data['id'])
                volunteer.status = "inactive"
                volunteer.save()
                send_mail(
                    subject='Inactive',
                    message='Your application is inactive',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.RECIPIENT_ADDRESS]
                )


                return HttpResponse(status=200)

    def get(self, request, status = ""):
        if request.method == 'GET':
            if status == "":
                volunteers = Volunteers.objects.all()
                serializer = volunteerSerializer(volunteers, many=True)
            else:
                volunteers = Volunteers.objects.filter(status=status)
                serializer = volunteerSerializer(volunteers, many=True)
        return JsonResponse(serializer.data, safe=False)


class userType(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':
            user = request.user
            if user.is_staff:
                return JsonResponse({"userType": "staff"}, safe=False)
            else:
                return JsonResponse({"userType": "volunteer"}, safe=False)


class pickedUp(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            pickedUp_data = JSONParser().parse(request)
            volunteer = request.user
            pickedUp_data['volunteer'] = volunteer.id
            # pickedUp_data['range_to'] = str(int(pickedUp_data['range_from']) + int(pickedUp_data['amount']))
            volunteer.couponAmount = volunteer.couponAmount + int(pickedUp_data['amount'])

            couponsSerializer = volunteerCouponSerializer(data=pickedUp_data)
            serializer = pikedUpSerializer(data=pickedUp_data)
            if serializer.is_valid():
                serializer.save()
                volunteer.save()
            if couponsSerializer.is_valid():
                couponsSerializer.save()
                return HttpResponse(status=200)

            print(serializer.errors)
            return HttpResponse(status=400)

    def get(self, request):
        if request.method == 'GET':
            volunteer = request.user
            pickups = PickedUp.objects.filter(volunteer=volunteer)
            serializer = pikedUpSerializer(pickups, many=True)
            return JsonResponse(serializer.data, safe=False)


class registerCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            company_data = JSONParser().parse(request)
            company_data['volunteer'] = request.user.id
            company_data['branch'] = branch.objects.get(name=company_data['branch']).id
            if Companies.objects.filter(companyName=company_data['companyName']).exists():
                return HttpResponse(status=400)
            serializer = companySerializer(data=company_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)

            print(serializer.errors)
            return HttpResponse(status=400)

    def get(self, request, id=0):
        if request.method == 'GET':
            if (id == 0):
                volunteer = request.user
                companies = Companies.objects.filter(branch=volunteer.branch)
                serializer = companySerializer(companies, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                company = Companies.objects.get(id=id)
                serializer = companySerializer(company)
                return JsonResponse(serializer.data, safe=False)
            



class discardLost(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            discardLost_data = JSONParser().parse(request)
            volunteer = request.user
            discardLost_data['volunteer'] = volunteer.id
            flag = False
            flag_reason = ""

            if (
            not (((volunteerCoupons.objects.filter(volunteer=volunteer, serial_letter=discardLost_data['serial_letter'],
                                                   range_from__lte=discardLost_data['range_from'],
                                                   range_to__gte=discardLost_data['range_to'])).exists())
            )):
                flag = True
                flag_reason = "Volunteer does not have the coupons"
                print("flag is true")

            # check if they are already discarded
            if (discardLostModel.objects.filter(volunteer=volunteer, serial_letter=discardLost_data['serial_letter'],
                                                range_from__lte=discardLost_data['range_from'],
                                                range_to__gte=discardLost_data['range_to'])).exists():
                flag = True
                flag_reason = "Coupons already discarded"
                print("flag is true")

            discardLost_data['flag'] = flag
            volunteer.couponAmount = volunteer.couponAmount - int(discardLost_data['amount'])
            if (not flag):
                coupons = volunteerCoupons.objects.filter(volunteer=volunteer,
                                                          serial_letter=discardLost_data['serial_letter'],
                                                          range_from__lte=discardLost_data['range_from'],
                                                          range_to__gte=discardLost_data['range_to'])
                for coupon in coupons:
                    if (coupon.range_from == discardLost_data['range_from'] and coupon.range_to == discardLost_data[
                        'range_to'] and coupons.count() == 1):
                        coupon.delete()
                        break
                    else:
                        if (coupon.range_from == discardLost_data['range_from']):
                            coupon.range_from = discardLost_data['range_to'] + 1
                            coupon.save()
                            break
                        elif (coupon.range_to == discardLost_data['range_to']):
                            coupon.range_to = discardLost_data['range_from'] - 1
                            coupon.save()
                            break
                        else:
                            newCoupon = volunteerCouponSerializer.objects(volunteer=volunteer,
                                                                                 serial_letter=discardLost_data[
                                                                                     'serial_letter'],
                                                                                 range_from=coupon.range_from,
                                                                                 range_to=discardLost_data[
                                                                                              'range_from'] - 1)
                            newCoupon.save()
                            coupon.range_from = discardLost_data['range_to'] + 1
                            coupon.save()
                            break

            serializer = discardLostSerializer(data=discardLost_data)
            if serializer.is_valid():
                serializer.save()
                volunteer.save()
                if (flag):
                    status = 201

                else:
                    status = 200

                return HttpResponse({"flag_reason": flag_reason}, status=status)

            print(serializer.errors)
            return HttpResponse(status=400)

    def get(self, request):
        if request.method == 'GET':
            volunteer = request.user
            discardLost = discardLostSerializer.objects.filter(volunteer=volunteer)
            serializer = discardLostSerializer(discardLost, many=True)
            return JsonResponse(serializer.data, safe=False)

    def get(self, request):
        if request.method == 'GET':
            volunteer = request.user
            discardLost = discardLostSerializer.objects.filter(volunteer=volunteer)
            serializer = discardLostSerializer(discardLost, many=True)
            return JsonResponse(serializer.data, safe=False)


class coupons(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request, status="", id=0):
        if request.method == 'GET':
            if status != "":
                coupons = OnlineCoupons.objects.filter(status=status).filter(branch=request.user.branch.name)
                coupon_serializer = transactionsSerializer(coupons, many=True)
                return JsonResponse(coupon_serializer.data, safe=False)
            elif id != 0:
                print(id)
                coupon = OnlineCoupons.objects.get(id=id)
                coupon_serializer = transactionsSerializer(coupon)
                return JsonResponse(coupon_serializer.data, safe=False)

    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def patch(self, request, id=0):
        if request.method == 'PATCH':
            coupon_data = JSONParser().parse(request)
            coupon = OnlineCoupons.objects.get(id=id)
            send_mail(
                subject=coupon_data['status'],
                message='Your order status from heartflow has been updated to ' + coupon_data['status'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[coupon.email]
            )
            coupon.status = coupon_data['status']
            coupon.save()
            return HttpResponse(status=200)


class exchange(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            exchange_data = JSONParser().parse(request)
            exchange_data["volunteer_from"] = request.user.id
            volunteer = request.user
            flag_reason = ""
            flag = False
            # check if valid exchange

            if (
            not (((volunteerCoupons.objects.filter(volunteer=volunteer, serial_letter=exchange_data['serial_letter'],
                                                   range_from__lte=exchange_data['range_from'],
                                                   range_to__gte=exchange_data['range_to'])).exists())
            )):
                flag = True
                flag_reason = "Volunteer does not have the coupons"
                print("flag is true")
            if (not flag):
                coupons = volunteerCoupons.objects.filter(volunteer=volunteer,
                                                          serial_letter=exchange_data['serial_letter'],
                                                          range_from__lte=exchange_data['range_from'],
                                                          range_to__gte=exchange_data['range_to'])
                for coupon in coupons:
                    if (coupon.range_from == exchange_data['range_from'] and coupon.range_to == exchange_data[
                        'range_to'] and coupons.count() == 1):
                        coupon.delete()
                        break
                    else:
                        if (coupon.range_from == exchange_data['range_from']):
                            coupon.range_from = exchange_data['range_to'] + 1
                            coupon.save()
                            break
                        elif (coupon.range_to == exchange_data['range_to']):
                            coupon.range_to = exchange_data['range_from'] - 1
                            coupon.save()
                            break
                        else:
                            newCoupon = volunteerCoupons.objects(volunteer=volunteer,
                                                                        serial_letter=exchange_data['serial_letter'],
                                                                        range_from=coupon.range_from,
                                                                        range_to=exchange_data['range_from'] - 1)
                            newCoupon.save()
                            coupon.range_from = exchange_data['range_to'] + 1
                            coupon.save()
                            break

                couponsTo = volunteerCoupons(volunteer=exchange_data["volunteer_to"],
                                                    serial_letter=exchange_data['serial_letter'],
                                                    range_from=exchange_data['range_from'],
                                                    range_to=exchange_data['range_to'])
                couponsTo.save()

            exchange_data['from_volunteer'] = volunteer.id
            serializer = exchangeSerializer(data=exchange_data)
            if serializer.is_valid():
                serializer.save()
                if (flag):
                    status = 201
                else:
                    status = 200
                return HttpResponse({"flag_reason": flag_reason}, status=status)

            print(serializer.errors)
            return HttpResponse(status=400)


class deliver(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            deliver_data = JSONParser().parse(request)
            volunteer = request.user
            deliver_data['volunteer'] = volunteer.id
            serializer = deliverySerializer(data=deliver_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)

            print(serializer.errors)
            return HttpResponse(status=400)

    def get(self, request):
        if request.method == 'GET':
            volunteer = request.user
            deliver = deliverySerializer.objects.filter(volunteer=volunteer)
            serializer = deliverySerializer(deliver, many=True)
            return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def resetPassword(request, token):
    if request.method == 'POST':
        token = decode_reset_token(token)
        data = JSONParser().parse(request)
        if token:
            volunteer = Volunteers.objects.get(id=token)
            volunteer.password = make_password(data['password'])
            volunteer.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


@csrf_exempt
def branchCRUD(request):
    if request.method == 'POST':
        branch_data = JSONParser().parse(request)
        serializer = branchSerializer(data=branch_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)

        print(serializer.errors)
        return HttpResponse(status=201)

    if request.method == 'GET':
        branches = branch.objects.all()
        branch_serializer = branchSerializer(branches, many=True)
        return JsonResponse(branch_serializer.data, safe=False)
    # elif request.method == 'GET':


class sources(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.method == 'GET':
            volunteer = request.user
            sources = source.objects.filter(branch_source=volunteer.branch)
            serializer = sourceSerializer(sources, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if request.method == 'POST':
            source_data = JSONParser().parse(request)
            serializer = sourceSerializer(data=source_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status=200)

            print(serializer.errors)
            return HttpResponse(status=400)


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.
    
    @see https://djangosnippets.org/snippets/2215/
    """
    related_subtype = 'related'

    def __init__(self, *args, **kwargs):
        # self.related_ids = []
        self.related_attachments = []
        return super(EmailMultiRelated, self).__init__(*args, **kwargs)

    def attach_related(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if isinstance(filename, MIMEBase):
            assert content == mimetype == None
            self.related_attachments.append(filename)
        else:
            assert content is not None
            self.related_attachments.append((filename, content, mimetype))

    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        print(mimetypes.guess_type(os.path.basename(path)))
        self.attach_related(filename, content, mimetypes.guess_type(os.path.basename(path))[0])

    def _create_message(self, msg):
        return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))

    def _create_alternatives(self, msg):
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == 'text/html':
                for related_attachment in self.related_attachments:
                    if isinstance(related_attachment, MIMEBase):
                        content_id = related_attachment.get('Content-ID')
                        content = re.sub(r'(?<!cid:)%s' % re.escape(content_id), 'cid:%s' % content_id, content)
                    else:
                        filename, _, _ = related_attachment
                        content = re.sub(r'(?<!cid:)%s' % re.escape(filename), 'cid:%s' % filename, content)
                self.alternatives[i] = (content, mimetype)

        return super(EmailMultiRelated, self)._create_alternatives(msg)

    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related_attachment in self.related_attachments:
                if isinstance(related_attachment, MIMEBase):
                    msg.attach(related_attachment)
                else:
                    msg.attach(self._create_related_attachment(*related_attachment))
        return msg

    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del (attachment['Content-Type'])
            del (attachment['Content-Disposition'])
            attachment.add_header('Content-Disposition', 'inline', filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename)
        return attachment
