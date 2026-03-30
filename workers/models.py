from django.db import models


# ---------------------------------------------------------------------------
# Choices — defined at module level so forms and admin can reuse them
# ---------------------------------------------------------------------------

NHS_BANDS = [
    ('2',  'Band 2'),
    ('3',  'Band 3'),
    ('5',  'Band 5'),
    ('6',  'Band 6'),
    ('7',  'Band 7'),
    ('8a', 'Band 8a'),
]

RIGHT_TO_WORK_CHOICES = [
    ('uk_citizen',  'UK Citizen'),
    ('eu_settled',  'EU Settled'),
    ('work_visa',   'Work Visa'),
    ('other',       'Other'),
]

WORKER_STATUS_CHOICES = [
    ('available', 'Available'),
    ('on_shift',  'On Shift'),
    ('off',       'Off'),
]


# ---------------------------------------------------------------------------
# Worker — a healthcare professional managed by an Agency user
# ---------------------------------------------------------------------------

class Worker(models.Model):
    # Personal details
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20)

    # Professional details
    role         = models.CharField(max_length=200)
    nhs_band     = models.CharField(max_length=5, choices=NHS_BANDS)
    nmc_pin      = models.CharField(max_length=20, unique=True, help_text="NMC registration number e.g. 21A3847E")
    right_to_work = models.CharField(max_length=50, choices=RIGHT_TO_WORK_CHOICES)
    skills       = models.TextField(blank=True, help_text="Comma-separated, e.g. ICU, ACLS, Ventilator")

    # Status & performance
    status           = models.CharField(max_length=20, choices=WORKER_STATUS_CHOICES, default='available')
    rating           = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    shifts_completed = models.PositiveIntegerField(default=0)

    # Ownership — which agency added this worker
    agency = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='workers',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} — Band {self.nhs_band}"

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_initials(self):
        """Return two-letter initials, e.g. 'JO' for James Okafor."""
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    def get_skills_list(self):
        """Return the skills string as a clean Python list."""
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
