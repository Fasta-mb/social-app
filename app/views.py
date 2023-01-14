from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from app.forms import CommentForm, PostForm, ProfileForm, ReportForm
from app.models import Comment, Post, ProfileUser
from django.core import mail
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    posts = Post.objects.all()
    postnavs = Post.objects.all().order_by('-created')[0:3]
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    searches = Post.objects.filter(
        Q(author__username__icontains=q) |
        Q(title__icontains=q)
    )
    context = {
        'posts': posts,
        'q': q,
        'searches': searches,
        'postnavs': postnavs,
        }
    return render(request, 'app/index.html', context)

def createProfile(request):
    # if request.user.is_authenticated:
    #     return redirect(reverse('home'))
    if request.user.username == '':
        return redirect(reverse('register'))
    
    print(request.user.username == '')
    
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            return redirect(reverse('home'))
            
    else:
        form = ProfileForm()
            
    context = {'form': form}
    return render(request, 'app/create_profile.html', context)

@login_required(login_url='login')
def profileUser(request):
    user = request.user
    profile = ProfileUser.objects.filter(user=user)
    posts = Post.objects.filter(author=user)
    postnavs = Post.objects.all().order_by('-created')[0:3]
    context = {
        'profile': profile, 
        'posts': posts,
        'postnavs': postnavs
        }
    return render(request, 'app/profileUser.html', context)

@login_required(login_url='login')
def updateProfileUser(request):
    postnavs = Post.objects.all().order_by('-created')[0:3]
    if request.method == 'POST':
        profile = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profileuser)
        if profile.is_valid():
            profile.save()
            return redirect(reverse('profile-user'))
    else:
        profile = ProfileForm(instance=request.user.profileuser)
    
    return render(request, 'app/profileUserEdit.html', {'profile': profile, 'postnavs':postnavs})

@login_required(login_url='login')
def post(request):
    postnavs = Post.objects.all().order_by('-created')[0:3]
    
    if request.method == 'POST':
        post = PostForm(data=request.POST, files=request.FILES)
        if post.is_valid():
            post_save = post.save(commit=False)
            post_save.author = request.user
            post_save.slug = post_save.title
            post_save.picuser = ProfileUser.objects.get(user=request.user)
            post_save.save()
            return redirect(reverse('home'))
    else:
        post = PostForm(data=request.POST, files=request.FILES)
        
    context = {
        'post': post,
        'postnavs': postnavs
        }
    return render(request, 'app/post.html', context)

def postView(request, slug):
    view = Post.objects.get(slug=slug)
    comments = view.comment_set.all()
    comment_count = comments.count()
    comment = CommentForm(data=request.GET)
    postnavs = Post.objects.all().order_by('-created')[0:3]
    
    if request.method == 'POST':
        comment = CommentForm(data=request.POST)
        if request.user.is_authenticated:
            if comment.is_valid():
                comment_save = comment.save(commit=False)
                comment_save.author = request.user
                comment_save.post = view
                comment_save.pic = ProfileUser.objects.get(user=request.user)
                comment_save.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            else:
                comment = CommentForm(data=request.GET)
        else:
            return redirect(reverse('login'))
   
    context = {'view': view, 
               'comment': comment,
               'comments': comments,
               'comment_count': comment_count,
               'postnavs': postnavs
               }
    return render(request, 'app/post_view.html', context)

def editComment(request, pk):
    comment = Comment.objects.get(id=pk)
    

    if request.method == 'POST':
        editC = CommentForm( instance=comment, data=request.POST)
        if editC.is_valid():
            editC.save()
            return HttpResponseRedirect(reverse('post-view', kwargs={'slug': comment.post.slug}))
    else:
        editC = CommentForm(instance=comment)
        
    context = {'editC': editC}
    
    return render(request, 'app/comment_edit.html', context)

def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return HttpResponseRedirect(reverse('post-view', kwargs={'slug': comment.post.slug}))


def sendReport(request):
    if request.method == 'POST':
        report = ReportForm(request.POST)
    
        print(report['subject'])
        if report.is_valid():
            subject = report.cleaned_data['subject']
            message = report.cleaned_data['message']
            email = report.cleaned_data['email']
    
            with mail.get_connection() as connection:
                mail.EmailMessage(
                subject, message, email, ['fastamb@gmail.com'],
                connection=connection,
                ).send()
                return redirect(reverse('home'))
            
    else:
        report = ReportForm()
        
    context = {'report': report}
    return render(request, 'app/report.html', context)

def deleteAccount(request):
    postnavs = Post.objects.all().order_by('-created')[0:3]
    return render(request, 'app/deleteAccountConf.html', {'postnavs': postnavs})

def confDeleteAccount(request):
    if request.user.is_authenticated:
        request.user.delete()
        return redirect(reverse('register'))
    
    
def notification(request):
    posts = Post.objects.all().order_by('-created')[0:3]
    
    context = {'posts': posts}
    return render(request, 'app/index.html', context)
    