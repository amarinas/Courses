from django.shortcuts import render, redirect
from .models import Course, Description, Comment
from django.contrib import messages

# Create your views here.

# Render the home page
def index(request):

    context = {
        'courses': Course.objects.all(),
        'descriptions': Description.objects.all()
    }
    return render(request, 'courseList/index.html', context)

# Add a course to the course list
def addCourse(request):
    if len(request.POST['name']) <= 0 and len(request.POST['description']) <=0:
        messages.add_message(request, messages.INFO, 'Cannot leave this empty or my database will blow up')
        return redirect('/')
    else:

        c = Course.objects.create(name=request.POST['name'])
        instance = Course.objects.get(id=c.id)
        Description.objects.create(course_id=instance, description=request.POST['description'])
        return redirect('/')

# Render the delete course confirmation page
def delCourse(request, id):
    courseInst = Course.objects.get(id=id)
    context = {
        'course': courseInst,
        'description': Description.objects.get(course_id=courseInst)
    }
    return render(request, "courseList/destroy.html", context)

# Delete a course
def deleteC(request):
    Course.objects.get(id=request.POST['id']).delete()
    return redirect('/')

# Render the comments page
def seeComments(request, id):
    course = Course.objects.get(id=id)
    comments = Comment.objects.filter(course=course).order_by('created_at')
    context = {
        'course': course,
        'comments': comments
    }
    return render(request, 'courseList/comments.html', context)

# Add a comment
def addComment(request):

        course = Course.objects.get(id=request.POST['id'])
        Comment.objects.create(course=course, comment=request.POST['commentbox'])
        url_str = "courses/comment/" + str(request.POST['id'])
        return redirect(url_str)
