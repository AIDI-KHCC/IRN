# review/models.py

from django.db import models
from django.contrib.auth.models import User
from submission.models import Submission
from forms_builder.models import DynamicForm
from datetime import datetime

class ReviewRequest(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    submission_version = models.PositiveIntegerField(
        help_text="Version number of the submission being reviewed"
    )
    requested_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='review_requests_created'
    )
    requested_to = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='review_requests_received'
    )
    message = models.TextField(blank=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
            ('completed', 'Completed')
        ],
        default='pending'
    )
    selected_forms = models.ManyToManyField(DynamicForm)
    conflict_of_interest_declared = models.BooleanField(null=True)
    conflict_of_interest_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure submission_version is an integer
        if isinstance(self.submission_version, datetime):
            self.submission_version = self.submission.version
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review Request for {self.submission} (Version {self.submission_version})"

class Review(models.Model):
    review_request = models.ForeignKey(ReviewRequest, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    submission_version = models.PositiveIntegerField()
    comments = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.submission}"

class FormResponse(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    form = models.ForeignKey(DynamicForm, on_delete=models.CASCADE)
    response_data = models.JSONField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.form} for {self.review}"