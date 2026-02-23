from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    PIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    STATUS_CHOICES = [
        ('O', 'Open'),
        ('IP', 'In Progress'),
        ('DO', 'Done'),

    ]

    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    due_date = models.DateTimeField(verbose_name='Due Time')

    priority = models.CharField(
        max_length=1, choices=PIORITY_CHOICES, verbose_name='Priority')

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default='O', verbose_name='Status')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created At')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='User')

    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="tasks", verbose_name="project")

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_overdue(self):
        '''Check if the task is overdue.'''
        if self.due_date and self.status != 'DO':
            return timezone.now() > self.due_date

        return False
