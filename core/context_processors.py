from shifts.models import Assignment, Shift


def global_context(request):
    """
    Inject notification counts into every template automatically.
    Django calls this for every request because it's listed in
    settings.py → TEMPLATES → OPTIONS → context_processors.

    Returns an empty dict for unauthenticated users so the
    sidebar badges simply don't appear on the login page.
    """
    if not request.user.is_authenticated:
        return {}

    return {
        # Red badge on Assignments nav item
        'pending_notifications': Assignment.objects.filter(status='pending').count(),
        # Orange badge on Available Shifts nav item
        'urgent_shifts':         Shift.objects.filter(status='urgent').count(),
    }
