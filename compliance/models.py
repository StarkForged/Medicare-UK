from django.db import models


# ---------------------------------------------------------------------------
# Choices
# ---------------------------------------------------------------------------

DOCUMENT_STATUS_CHOICES = [
    ('valid',    'Valid'),
    ('expiring', 'Expiring Soon'),
    ('expired',  'Expired'),
]

DOCUMENT_TYPE_CHOICES = [
    ('dbs',               'DBS Certificate'),
    ('nmc',               'NMC Certificate'),
    ('bls',               'BLS / CPR'),
    ('manual_handling',   'Manual Handling'),
    ('infection_control', 'Infection Control'),
    ('rtw',               'Right to Work'),
    ('passport',          'Passport / ID'),
    ('other',             'Other'),
]


# ---------------------------------------------------------------------------
# ComplianceDocument — a single compliance/certification document for a worker
# ---------------------------------------------------------------------------

class ComplianceDocument(models.Model):
    worker      = models.ForeignKey(
        'workers.Worker',
        on_delete=models.CASCADE,
        related_name='documents',
    )
    doc_type    = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    title       = models.CharField(max_length=200)
    issued_by   = models.CharField(max_length=200, blank=True)
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    file        = models.FileField(upload_to='documents/', null=True, blank=True)
    status      = models.CharField(max_length=10, choices=DOCUMENT_STATUS_CHOICES, default='valid')
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['expiry_date']

    def __str__(self):
        return f"{self.get_doc_type_display()} — {self.worker}"
