from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ProjectForm, ReviewForm
from .models import Project

def project_list(request):
    projects = Project.objects.all()  # pyright: ignore
    search_query = request.GET.get('q', '')
    if search_query:
        projects = projects.filter(title_icontains=search_query)
    return render(request, 'project_review_app/project_list.html', {'projects':projects})

@login_required
def upload_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_review_app/upload_project.html', {'form': form})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    reviews = project.reviews.all()
    review_form = ReviewForm()
    return render(request, 'project_review_app/project_detail.html', {'project': project, 'reviews': reviews, 'review_form': review_form})

@login_required
def add_project_review(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.project = project
            review.save()
            return redirect('project_detail', pk=pk)
    else:
        redirect('project_detail', pk=pk)
