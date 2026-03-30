from django.db import models
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Choices — defined at module level so they can be reused in forms/admin too
# ---------------------------------------------------------------------------

URGENCY_CHOICES = [
    ('low',    'Low'),
    ('medium', 'Medium'),
    ('high',   'High / Urgent'),
]

SHIFT_STATUS_CHOICES = [
    ('open',        'Open'),
    ('in_progress', 'In Progress'),
    ('filled',      'Filled'),
    ('urgent',      'Urgent'),
]

ASSIGNMENT_STATUS_CHOICES = [
    ('pending',   'Pending Approval'),
    ('confirmed', 'Confirmed'),
    ('rejected',  'Rejected'),
    ('completed', 'Completed'),
]


# ---------------------------------------------------------------------------
# NHSTrust — represents a hospital / NHS organisation
# ---------------------------------------------------------------------------

class NHSTrust(models.Model):
    name          = models.CharField(max_length=200)
    location      = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Shift — a single shift slot posted by an NHS Trust
# ---------------------------------------------------------------------------

class Shift(models.Model):
    trust           = models.ForeignKey(NHSTrust, on_delete=models.CASCADE, related_name='shifts')
    role            = models.CharField(max_length=200)
    department      = models.CharField(max_length=200)
    nhs_band        = models.CharField(max_length=5)
    date            = models.DateField()
    start_time      = models.TimeField()
    end_time        = models.TimeField()
    pay_rate        = models.DecimalField(max_digits=8, decimal_places=2)
    required_skills = models.TextField(blank=True)
    urgency         = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='low')
    status          = models.CharField(max_length=20, choices=SHIFT_STATUS_CHOICES, default='open')
    notes           = models.TextField(blank=True)
    created_by      = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.role} — {self.trust.name} — {self.date}"

    def get_duration_hours(self):
        """
        Return the shift length in whole hours.
        Handles overnight shifts (e.g. 20:00 – 08:00) by adding a day
        when end_time is before start_time.
        BUG FIX: original used .seconds which caps at 86399 (23h 59m).
        total_seconds() works correctly for multi-day durations too.
        """
        start = datetime.combine(self.date, self.start_time)
        end   = datetime.combine(self.date, self.end_time)

        if end < start:                  # overnight shift
            end += timedelta(days=1)

        total_seconds = (end - start).total_seconds()
        return int(total_seconds // 3600)

    def get_skills_list(self):
        """Return required_skills as a clean Python list (split on comma)."""
        if not self.required_skills:
            return []
        return [skill.strip() for skill in self.required_skills.split(',') if skill.strip()]


# ---------------------------------------------------------------------------
# Assignment — links a Worker to a Shift, created by an Agency user
# ---------------------------------------------------------------------------

class Assignment(models.Model):
    shift       = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='assignments')
    worker      = models.ForeignKey('workers.Worker', on_delete=models.CASCADE, related_name='assignments')
    agency      = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    status      = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS_CHOICES, default='pending')
    match_score = models.IntegerField(default=0, help_text="Skill match score 0–100")
    notes       = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.worker} → {self.shift}"
