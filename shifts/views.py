from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Shift, Assignment
from .forms import ShiftForm


@login_required
def shift_list(request):
    """Show all shifts that are still open or marked urgent."""
    shifts = Shift.objects.filter(
        status__in=['open', 'urgent']
    ).select_related('trust')   # select_related avoids N+1 queries for trust name

    return render(request, 'shifts/list.html', {'shifts': shifts})


@login_required
def shift_detail(request, pk):
    """Show the detail page for a single shift."""
    shift = get_object_or_404(Shift, pk=pk)
    return render(request, 'shifts/detail.html', {'shift': shift})


@login_required
def shift_create(request):
    """
    POST  → validate form, save shift, redirect to shift list.
    GET   → show the empty form.
    """
    form = ShiftForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shift = form.save(commit=False)   # don't save to DB yet
        shift.created_by = request.user   # attach the logged-in user
        shift.save()
        messages.success(request, "Shift posted successfully.")
        return redirect('shifts:list')

    return render(request, 'shifts/form.html', {
        'form':  form,
        'title': 'Post a New Shift',
    })


@login_required
def assignment_list(request):
    """
    Show all assignments made by the current agency user.
    select_related('shift__trust', 'worker') fetches related rows in one
    SQL JOIN instead of separate queries per row.
    """
    assignments = Assignment.objects.filter(
        agency=request.user
    ).select_related('shift__trust', 'worker')

    return render(request, 'shifts/assignments.html', {'assignments': assignments})


@login_required
def assign_worker(request, shift_pk):
    """
    GET  → show the list of available workers so the agency can pick one.
    POST → create an Assignment linking the chosen worker to this shift.
    """
    from workers.models import Worker  # local import avoids circular import at module level

    shift = get_object_or_404(Shift, pk=shift_pk)

    if request.method == 'POST':
        worker_pk = request.POST.get('worker_id')
        worker    = get_object_or_404(Worker, pk=worker_pk, agency=request.user)

        # Prevent duplicate pending assignments for the same shift+worker
        already_assigned = Assignment.objects.filter(
            shift=shift, worker=worker, status='pending'
        ).exists()

        if already_assigned:
            messages.warning(request, f"{worker.get_full_name()} is already pending for this shift.")
        else:
            Assignment.objects.create(
                shift=shift,
                worker=worker,
                agency=request.user,
            )
            messages.success(request, f"{worker.get_full_name()} assigned to {shift.role}. Awaiting trust approval.")
            return redirect('shifts:assignments')

    # GET — load workers belonging to this agency
    workers = Worker.objects.filter(agency=request.user, status='available')
    return render(request, 'shifts/assign.html', {
        'shift':   shift,
        'workers': workers,
    })
