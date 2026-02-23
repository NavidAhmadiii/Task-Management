from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Project Name")
    descriptions = models.TextField(blank=True, verbose_name='description')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="owned_projects", verbose_name="owner")
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects", verbose_name="member")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(
        auto_now_add=True, verbose_name="updated_at")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name
    
    
