from __future__ import absolute_import

import logging
from datetime import datetime, timedelta
import pytz
from django.core.mail.message import EmailMessage
from django.template import loader
from edx_proctoring.models import ProctoredExamStudentOTP
from edx_proctoring.api import get_exam_attempt
from edx_proctoring.views import ProctoredAPIView

def update_otp_status(otp, status):
    pass

def _check_for_otp_timeout(otp):
    """
        Helper method for checking
        one time password has expiration
    """
    if not otp
        return None

    now_utc = datetime.now(pytz.UTC)
    has_otp_expired = now_utc > otp.expires_at

    if has_otp_expired:
        otp.status = 'expired'
        otp.save()
        otp = None
    return otp

def get_student_otp(exam_obj, user, otp):
    if not exam_obj
        return None
    exam_otp_obj = ProctoredExamStudentOTP.get_otp(exam=exam_obj, user=user, otp=otp)
    otp = _check_for_otp_timeout(exam_otp_obj)
    return otp

def is_otp_activated(exam, user_id):
    user = User.objects.get(id=user_id)
    return ProctoredExamStudentOTP.exits(exam=exam, user=user, status='activated')

# pylint: disable=inconsistent-return-statements
def _get_student_otp_view():
    """
    Returns a rendered view for the student one time password view
    """
    student_view_template = 'otp/entrance.html'
    return student_view_template

# function to generate OTP 
def _OTPgen():
  
    # Declare a string variable   
    # which stores all alpha-numeric characters 
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    varlen= len(string) 
    for i in range(6): 
        OTP += string[m.floor(r.random() * varlen)] 
    return (OTP) 

def generate_student_otp(exam, user):
    otp = None
    while otp is None:
        try:
            now_utc = datetime.now(pytz.UTC)
            expires = now_utc + datetime.timedelta(minutes = 10)
            otp = ProctoredExamStudentOTP.object.create(
                exam=exam,
                user=user,
                otp=_OTPgen(),
                created_at=now_utc,
                expires_at=expires,
                status='created'
                )
        except:
            pass

    return otp

def send_otp_email(user, otp):
    pass

class StudentProctoredExamOTP(ProctoredAPIView):
    """
    Endpoint for the StudentProctoredExamOTP
    /edx_proctoring/v1/proctored_exam/otp

    Supports:
        HTTP POST: Submit otp code 

    HTTP POST
    create an exam otp
    Expected POST data: {
        "exam_id": "1",
        "external_id": "123",
        "otp": "abcdef"
    }
    """

    def post(self, request):
        """
        HTTP POST handler. To create an exam otp.
        """
        exam_id = request.data.get('exam_id', None)
        otp = request.data.get('otp', None)
        exam = get_exam_by_id(exam_id)
        user = request.user
        otp_obj = get_student_otp(exam, user, otp)
        if (not otp_obj):
            raise ProctoredExamPermissionDenied(
                u'Attempted to access expired exam with exam_id {exam_id}'.format(exam_id=exam_id)
            )
        
        update_otp_status(otp_obj, status='')

        data = {'exam_id': exam_id}
        return Response(data)

class StudentProctoredExamRequestOTP(ProctoredAPIView):
    """
    Endpoint for the StudentProctoredExamOTP
    /edx_proctoring/v1/proctored_exam/otp/request/

    Supports:
        HTTP POST: create otp code 

    HTTP POST
    create an exam otp
    Expected POST data: {
        "exam_id": "1",
        "external_id": "123",
    }
    """

    def post(self, request):
        """
        HTTP POST handler. To create an exam create a new otp.
        """
        exam_id = request.data.get('exam_id', None)
        exam = get_exam_by_id(exam_id)
        user = request.user
        otp = generate_student_otp(exam, user)
        send_otp_email(user, otp)
        data = {'exam_id': exam_id}
        return Response(data)
