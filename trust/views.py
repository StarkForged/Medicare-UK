from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from shifts.models import Shift, Assignment


@login_required
def trust_dashboard(request):
    """
    NHS Trust dashboard — shows shift stats and pending approval count.

    BUG FIX: original passed `pending_count` to the template but the
    template referenced `pending_approvals`. Now consistent.
    """
    context = {
        'open_shifts':       Shift.objects.filter(status='open').count(),
        'pending_approvals': Assignment.objects.filter(status='pending').count(),
        'filled_shifts':     Shift.objects.filter(status='filled').count(),
        'recent_shifts':     Shift.objects.all().select_related('trust')[:10],
    }
    return render(request, 'trust/dashboard.html', context)


@login_required
def trust_shifts(request):
    """Show all shifts (for the Trust to manage their own postings)."""
    shifts = Shift.objects.all().select_related('trust')
    return render(request, 'trust/shifts.html', {'shifts': shifts})


@login_required
def trust_approvals(request):
    """Show all pending assignments waiting for Trust approval."""
    assignments = Assignment.objects.filter(
        status='pending'
    ).select_related('shift__trust', 'worker')

    return render(request, 'trust/approvals.html', {'assignments': assignments})


@login_required
def approve_assignment(request, pk):
    """Mark an assignment as confirmed and record the approval timestamp."""
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.status       = 'confirmed'
    assignment.confirmed_at = timezone.now()
    assignment.save()
    messages.success(request, "Assignment confirmed. Agency has been notified.")
    return redirect('trust:approvals')


@login_required
def reject_assignment(request, pk):
    """
    Reject an assignment and return the shift to 'open' status
    so agencies can assign a different worker.
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.status = 'rejected'
    assignment.save()

    # Put the shift back on the open market
    shift = assignment.shift
    shift.status = 'open'
    shift.save()

    messages.warning(request, "Assignment rejected. Shift returned to open.")
    return redirect('trust:approvals')
