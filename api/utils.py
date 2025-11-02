from api.models import StudentRegistration, ContactSubmission

def get_pending_registrations(request=None):
    """Returns count of pending student registrations"""
    count = StudentRegistration.objects.filter(is_approved=False).count()
    return count if count > 0 else None

def get_unread_messages(request=None):
    """Returns count of unread contact messages"""
    count = ContactSubmission.objects.filter(is_read=False).count()
    return count if count > 0 else None
