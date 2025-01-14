from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)
    report_link = models.URLField(blank=False, null=False)
    demo_link = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pyright: ignore
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    grades = models.PositiveIntegerField(default=3)  # pyright: ignore
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for project {self.project.title}"  # pyright: ignore
