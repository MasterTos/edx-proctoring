

# pylint: disable=inconsistent-return-statements
def _get_student_otp_view():
    """
    Returns a rendered view for the student one time password view
    """
    student_view_template = None
    attempt = get_exam_attempt(exam_id, user_id)
    has_time_expired = False
    pass