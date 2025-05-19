from django.db import models

# Create your models here.

class Case(models.Model):
    borrower_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    outstanding_amount = models.DecimalField(max_digits=10, decimal_places=2)
    visit_status = models.CharField(max_length=50)
    last_visit_date = models.DateField(null=True, blank=True)
    last_visit_remarks = models.TextField(blank=True)
    ptp = models.DateField(null=True, blank=True)
    next_action = models.CharField(max_length=255)
    priority = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.borrower_name} - {self.visit_status}"

class Visit(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField()
    time = models.TimeField()
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    borrower_met = models.BooleanField(null=True)
    visited_whom = models.CharField(max_length=255, blank=True)
    remarks = models.TextField(blank=True)
    payment_status = models.CharField(max_length=50, blank=True)
    amount_collected = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interaction_remarks = models.TextField(blank=True)
    ptp_date = models.DateField(null=True, blank=True)
    ptp_reason = models.TextField(blank=True)
    selfie = models.ImageField(upload_to='visit_selfies/', null=True, blank=True)

    def __str__(self):
        return f"Visit for {self.case.borrower_name} on {self.date}"
