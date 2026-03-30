from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import User
from shifts.models import NHSTrust, Shift, Assignment
from workers.models import Worker


def _is_admin(user):
    """Helper used by @user_passes_test to restrict views to admin users only."""
    return user.role == 'admin'


@login_required
@user_passes_test(_is_admin)
def platform_overview(request):
    """Show platform-wide counts for the admin."""
    context = {
        'total_workers':       Worker.objects.count(),
        'total_shifts':        Shift.objects.count(),
        'total_trusts':        NHSTrust.objects.count(),
        'total_users':         User.objects.count(),
        'open_shifts':         Shift.objects.filter(status='open').count(),
        'pending_assignments': Assignment.objects.filter(status='pending').count(),
    }
    return render(request, 'admin_panel/overview.html', context)


@login_required
@user_passes_test(_is_admin)
def user_management(request):
    """Show all users, grouped by role then surname."""
    users = User.objects.all().order_by('role', 'last_name')
    return render(request, 'admin_panel/users.html', {'users': users})


@login_required
@user_passes_test(_is_admin)
def trust_management(request):
    """Show all registered NHS Trusts."""
    trusts = NHSTrust.objects.all()
    return render(request, 'admin_panel/trusts.html', {'trusts': trusts})
