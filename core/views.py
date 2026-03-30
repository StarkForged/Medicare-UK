from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from shifts.models import Shift, Assignment
from workers.models import Worker
from compliance.models import ComplianceDocument


@login_required
def dashboard(request):
    """
    Route the user to the correct dashboard based on their role.

    Agency  → sees their workers, open shifts, assignments, compliance alerts.
    Trust   → sees shift counts and pending approvals.
    Admin   → redirected to the dedicated admin panel.
    """
    user = request.user

    if user.role == 'agency':
        return render(request, 'core/dashboard_agency.html', _agency_context(user))

    if user.role == 'trust':
        return render(request, 'core/dashboard_trust.html', _trust_context())

    if user.role == 'admin':
        return redirect('admin_panel:overview')

    # Fallback — show agency view for any unknown role
    return render(request, 'core/dashboard_agency.html', {})


# ---------------------------------------------------------------------------
# Private helpers — build the context dict for each dashboard type.
# Keeping them separate makes the main dashboard() function easy to read.
# ---------------------------------------------------------------------------

def _agency_context(user):
    """Return context data for the Agency dashboard."""
    return {
        'open_shifts':          Shift.objects.filter(status__in=['open', 'urgent']).count(),
        'active_assignments':   Assignment.objects.filter(agency=user, status='pending').count(),
        'total_workers':        Worker.objects.filter(agency=user).count(),
        'expiring_docs':        ComplianceDocument.objects.filter(
                                    worker__agency=user, status='expiring'
                                ).count(),
        # Limit to 5 rows — we only show a preview on the dashboard
        'recent_shifts':        Shift.objects.filter(
                                    status__in=['open', 'urgent']
                                ).select_related('trust')[:5],
        'recent_assignments':   Assignment.objects.filter(
                                    agency=user
                                ).select_related('shift__trust', 'worker')[:5],
    }


def _trust_context():
    """Return context data for the NHS Trust dashboard."""
    return {
        'open_shifts':      Shift.objects.filter(status='open').count(),
        'pending_approvals': Assignment.objects.filter(status='pending').count(),
        'filled_shifts':    Shift.objects.filter(status='filled').count(),
    }
