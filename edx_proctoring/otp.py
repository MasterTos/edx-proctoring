from .models import ProctoredExamStudentOTP

def _check_for_otp_timeout(otp):
    """
        Helper method for checking
        one time password has expiration
    """
    if not otp
        return None

    now_utc = datetime.now(pytz.UTC)
    expires_at = otp['expires_at']
    has_otp_expired = now_utc > expires_at

    if has_otp_expired:
        update_otp_status(
            otp['exam_attempt']['id'],
            status
        )
    return otp

def get_student_otp(exam_attempt_obj):
    if not exam_attempt_obj
        return None
    exam_otp_obj = ProctoredExamStudentOTP.objects.get(exam_attempt=exam_attempt_obj)
    otp = exam_otp_obj.data
    otp = _check_for_otp_timeout(otp)


# pylint: disable=inconsistent-return-statements
def _get_student_otp_view():
    """
    Returns a rendered view for the student one time password view
    """
    student_view_template = None
    attempt = get_exam_attempt(exam_id, user_id)
    has_time_expired = False
    pass