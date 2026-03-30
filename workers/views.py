from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Worker
from .forms import WorkerForm


@login_required
def worker_list(request):
    """Show all workers belonging to the logged-in agency user."""
    workers = Worker.objects.filter(agency=request.user)
    return render(request, 'workers/list.html', {'workers': workers})


@login_required
def worker_detail(request, pk):
    """
    Show a single worker's profile.
    `agency=request.user` ensures an agency can only view their own workers.
    """
    worker = get_object_or_404(Worker, pk=pk, agency=request.user)
    return render(request, 'workers/detail.html', {'worker': worker})


@login_required
def worker_add(request):
    """Create a new worker and attach them to the current agency."""
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)  # don't save yet
            worker.agency = request.user       # set the agency before saving
            worker.save()
            messages.success(request, f"{worker.get_full_name()} added to your roster.")
            return redirect('workers:list')
    else:
        form = WorkerForm()

    return render(request, 'workers/form.html', {'form': form, 'title': 'Add Worker'})


@login_required
def worker_edit(request, pk):
    """Edit an existing worker's details."""
    worker = get_object_or_404(Worker, pk=pk, agency=request.user)

    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker profile updated.")
            return redirect('workers:detail', pk=pk)
    else:
        form = WorkerForm(instance=worker)  # pre-fill form with existing data

    return render(request, 'workers/form.html', {
        'form':   form,
        'title':  'Edit Worker',
        'worker': worker,
    })
