from django import template

register = template.Library()


@register.filter
def stars(value):
    """
    Convert a numeric rating (e.g. 4.9) to a ★★★★☆ star string.
    Usage in template: {{ worker.rating|stars }}
    """
    try:
        filled = int(float(value))
        empty  = 5 - filled
        return ('★' * filled) + ('☆' * empty)
    except (ValueError, TypeError):
        return '☆☆☆☆☆'


@register.filter
def status_badge_class(status):
    """
    Map a status string to its CSS badge class.
    Usage: <span class="badge {{ assignment.status|status_badge_class }}">
    """
    mapping = {
        'open':        'b-open',
        'in_progress': 'b-progress',
        'filled':      'b-filled',
        'urgent':      'b-urgent',
        'pending':     'b-pending',
        'confirmed':   'b-filled',
        'rejected':    'b-urgent',
        'completed':   'b-filled',
        'valid':       'b-valid',
        'expiring':    'b-expiring',
        'expired':     'b-expired',
        'available':   'b-available',
        'on_shift':    'b-onshift',
        'off':         'b-off',
    }
    return mapping.get(status, 'b-open')
