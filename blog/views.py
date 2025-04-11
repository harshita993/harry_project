from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
def blog_list(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).order_by('-created_at')
    else:
        posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'posts': posts, 'query': query})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'post': post})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return redirect('blog_detail', pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('blog_list')
