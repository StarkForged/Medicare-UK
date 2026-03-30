from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends Django's built-in User.
    We add a `role` so the same login system works for
    Agency staff, NHS Trust staff, and Platform Admins.
    """

    # Role constants — use these instead of bare strings throughout the app
    ROLE_AGENCY = 'agency'
    ROLE_TRUST  = 'trust'
    ROLE_ADMIN  = 'admin'

    ROLE_CHOICES = [
        (ROLE_AGENCY, 'Agency Staff'),
        (ROLE_TRUST,  'NHS Trust'),
        (ROLE_ADMIN,  'Platform Admin'),
    ]

    role         = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_AGENCY)
    organisation = models.CharField(max_length=200, blank=True)
    phone        = models.CharField(max_length=20, blank=True)
    avatar       = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def get_initials(self):
        """Return 'AB' style initials from the user's full name."""
        parts = self.get_full_name().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.username[:2].upper()

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
