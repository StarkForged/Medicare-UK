"""
Management command: python manage.py seed_data

Creates three demo accounts plus sample NHS Trusts, Workers, and Shifts
so you can explore the system immediately after setup.

Run once after `python manage.py migrate`.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shifts.models import NHSTrust, Shift
from workers.models import Worker
from datetime import date, time

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data for development'

    def handle(self, *args, **kwargs):
        self._create_users()
        trusts = self._create_trusts()
        agency = User.objects.get(username='agency1')
        self._create_workers(agency)
        self._create_shifts(trusts, agency)
        self.stdout.write(self.style.SUCCESS(
            '\n✅  Sample data ready!'
            '\n   admin   / admin123   → Platform Admin'
            '\n   agency1 / agency123  → Agency Staff'
            '\n   trust1  / trust123   → NHS Trust'
        ))

    # ------------------------------------------------------------------

    def _create_users(self):
        # Superuser / Platform Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@medicare-uk.nhs', 'admin123',
                role='admin', first_name='Platform', last_name='Admin',
            )
            self.stdout.write('  Created: admin')

        # Agency user
        agency, created = User.objects.get_or_create(username='agency1', defaults={
            'email':        'sarah@stafftech.co.uk',
            'role':         'agency',
            'first_name':   'Sarah',
            'last_name':    'Mitchell',
            'organisation': 'StaffTech Agency',
        })
        if created:
            agency.set_password('agency123')
            agency.save()
            self.stdout.write('  Created: agency1')

        # Trust user
        trust_user, created = User.objects.get_or_create(username='trust1', defaults={
            'email':        'james@kingscollege.nhs.uk',
            'role':         'trust',
            'first_name':   'James',
            'last_name':    'Pemberton',
            'organisation': "King's College Hospital",
        })
        if created:
            trust_user.set_password('trust123')
            trust_user.save()
            self.stdout.write("  Created: trust1")

    def _create_trusts(self):
        trust_data = [
            ("King's College Hospital NHS Foundation Trust", "Denmark Hill, London SE5 9RS"),
            ("Guy's and St Thomas' NHS Foundation Trust",   "Westminster Bridge Road, London SE1 7EH"),
            ("Royal London Hospital",                       "Whitechapel Road, London E1 1FR"),
            ("St Thomas' Hospital",                         "Westminster Bridge Road, London SE1 7EH"),
        ]
        trusts = []
        for name, location in trust_data:
            trust, created = NHSTrust.objects.get_or_create(name=name, defaults={'location': location})
            if created:
                self.stdout.write(f'  Created trust: {name}')
            trusts.append(trust)
        return trusts

    def _create_workers(self, agency):
        workers_data = [
            # (first, last, role, band, nmc_pin, status, skills)
            ('James',  'Okafor', 'ICU Staff Nurse',   '6', '21A3847E', 'available', 'ICU, ACLS, Ventilator, Chest Drains'),
            ('Amara',  'Reeves', 'HDU Nurse',          '6', '19B2153F', 'available', 'HDU, BLS, IV Cannulation, ECG'),
            ('Thomas', 'Webb',   'Theatre Nurse',      '5', '22C4921G', 'on_shift',  'Theatre, Scrub, Anaesthetics'),
            ('Priya',  'Sharma', 'Band 7 Sister',      '7', '18D3672H', 'available', 'Ward Management, ICU, Leadership'),
        ]
        for first, last, role, band, nmc, status, skills in workers_data:
            _, created = Worker.objects.get_or_create(nmc_pin=nmc, defaults={
                'first_name':     first,
                'last_name':      last,
                'role':           role,
                'nhs_band':       band,
                'status':         status,
                'skills':         skills,
                'right_to_work':  'uk_citizen',
                'phone':          '+44 7700 000000',
                'email':          f'{first.lower()}.{last.lower()}@email.co.uk',
                'rating':         4.9,
                'agency':         agency,
            })
            if created:
                self.stdout.write(f'  Created worker: {first} {last}')

    def _create_shifts(self, trusts, created_by):
        if Shift.objects.exists():
            return  # don't duplicate shifts on re-run

        shifts_data = [
            # (trust_index, role, dept, band, date, start, end, pay, skills, urgency, status)
            (0, 'Band 6 ICU Nurse',     'Intensive Care Unit', '6', date(2025, 4, 10), time(7, 0),  time(19, 0), 26.40, 'ICU, ACLS, Ventilator', 'high',   'urgent'),
            (1, 'Band 5 Theatre Nurse', 'Main Theatre',        '5', date(2025, 4, 12), time(8, 0),  time(20, 0), 22.50, 'Theatre, Scrub',         'medium', 'open'),
            (2, 'Band 6 HDU Nurse',     'High Dependency Unit','6', date(2025, 4, 14), time(19, 0), time(7, 0),  24.00, 'HDU, BLS',               'low',    'open'),
            (3, 'Band 7 Sister',        'Medical Ward',        '7', date(2025, 4, 15), time(7, 0),  time(19, 0), 32.00, 'Ward Management',         'medium', 'open'),
        ]
        for trust_idx, role, dept, band, shift_date, start, end, pay, skills, urgency, status in shifts_data:
            Shift.objects.create(
                trust=trusts[trust_idx], role=role, department=dept,
                nhs_band=band, date=shift_date, start_time=start, end_time=end,
                pay_rate=pay, required_skills=skills,
                urgency=urgency, status=status, created_by=created_by,
            )
        self.stdout.write(f'  Created {len(shifts_data)} sample shifts')
