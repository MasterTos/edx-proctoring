from __future__ import absolute_import

import logging
from datetime import datetime, timedelta
import pytz
from django.core.mail.message import EmailMessage
from edx_proctoring import constants
from django.template import loader
from edx_proctoring.models import ProctoredExamStudentOTP, ProctoredExam
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
# from edx_proctoring.views import ProctoredAPIView

def update_otp_status(otp, status):
    pass

def _check_for_otp_timeout(otp):
    """
        Helper method for checking
        one time password has expiration
    """
    if not otp:
        return None

    now_utc = datetime.now(pytz.UTC)
    has_otp_expired = now_utc > otp.expires_at

    if has_otp_expired:
        otp.status = 'expired'
        otp.save()
        otp = None
    return otp

def get_student_otp(exam, user, otp):
    if not exam:
        return None
    exam_otp_obj = ProctoredExamStudentOTP.get_otp(exam=exam, user=user, otp=otp)
    otp = _check_for_otp_timeout(exam_otp_obj)
    return otp

def is_otp_activated(exam, user_id):
    user = User.objects.get(id=user_id)
    return ProctoredExamStudentOTP.objects.filter(exam=exam, user=user, status='activated').exists()

# pylint: disable=inconsistent-return-statements
def _get_student_otp_view():
    """
    Returns a rendered view for the student one time password view
    """
    student_view_template = 'otp/entrance.html'
    return student_view_template

# function to generate OTP 
def _OTPgen():
    import math
    import random
    # Declare a string variable   
    # which stores all alpha-numeric characters 
    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    varlen= len(string) 
    for i in range(6): 
        OTP += string[int(math.floor(random.random() * varlen))] 
    return OTP

def generate_student_otp(exam, user):
    otp = None
    # try:
    now_utc = datetime.now(pytz.UTC)
    expires = now_utc + timedelta(minutes = 10)
    otp = ProctoredExamStudentOTP.objects.create(
        exam=ProctoredExam.get_exam_by_id(exam),
        user=user,
        otp=_OTPgen(),
        created_at=now_utc,
        expires_at=expires,
        status='created'
        )
    # except:
    #     pass

    return otp

def send_otp_email(user, otp):
    email_subject = "Gennext exam OTP"
    email_template_path = 'otp/otp_send.html'
    email_template = loader.get_template(email_template_path)
    body = email_template.render({
        'username': user.username,
        'exam_name': otp.exam.exam_name,
        'otp': otp,
    })

    email = EmailMessage(
        body=body,
        from_email=constants.FROM_EMAIL,
        to=[user.email],
        subject=email_subject,
    )
    email.content_subtype = 'html'

    email.send()
