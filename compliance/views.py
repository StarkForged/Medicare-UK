from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ComplianceDocument
from .forms import ComplianceDocumentForm
from workers.models import Worker


@login_required
def compliance_overview(request):
    """
    Show all workers and their documents for the current agency.
    prefetch_related('documents') loads all documents in one extra query
    instead of one query per worker (avoids N+1 problem).
    """
    workers  = Worker.objects.filter(agency=request.user).prefetch_related('documents')
    expired  = ComplianceDocument.objects.filter(worker__agency=request.user, status='expired')
    expiring = ComplianceDocument.objects.filter(worker__agency=request.user, status='expiring')

    return render(request, 'compliance/overview.html', {
        'workers':  workers,
        'expired':  expired,
        'expiring': expiring,
    })


@login_required
def document_add(request, worker_pk):
    """
    Upload a compliance document for a specific worker.

    BUG FIX: The original passed `initial={'worker': worker}` which pre-fills
    the form field but does NOT set the value on save — the user still has to
    manually pick the worker in the dropdown.
    Fix: after form.is_valid(), set doc.worker explicitly before saving.
    """
    worker = get_object_or_404(Worker, pk=worker_pk, agency=request.user)

    if request.method == 'POST':
        form = ComplianceDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.worker = worker          # always attach to the correct worker
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('workers:detail', pk=worker_pk)
    else:
        form = ComplianceDocumentForm()

    return render(request, 'compliance/form.html', {'form': form, 'worker': worker})
