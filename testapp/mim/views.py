from django.http import HttpResponse, Http404
#from exam.models import Answer
from exam.views import is_moderator, my_render_to_response, my_redirect
from exam.models import *
from django.contrib.auth import login, logout, authenticate
#from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mim_fetch_user import *
from mim_transfer_result import *

from exam.models import Quiz, Question, QuestionPaper
from exam.models import Profile, Answer, AnswerPaper, User, SpokenTutorialUser
from django.contrib.auth.models import User
from mim.models import * 

# Create your views here.
moodle_id=[]
foss = []
testcode = []

def index(request):
    """ The start page.
    """
    user=request.user
    if not user.is_authenticated() or not is_moderator(user):
        raise Http404("You are not allowed to view this page")
    """ if request.method == "POST":
        if "Fetch" in request.POST:
            print "Fetch"
            moodle_id, foss, testcode = fetch()
            for (a,b,c) in zip(moodle_id, foss, testcode):
                 print a,b,c

        if "Insert" in request.POST:
            print "Insert"
            fetch_password()
        if "View" in request.POST:
            print "View"
            insert_django()
    """
    #c= Answer.objects.get(id=1194)
    #print c.marks
    #return HttpResponse(c.marks)
    return render_to_response('mim.html',{}, 
                              context_instance=RequestContext(request))


def fetch(request):
    user = request.user
    if not user.is_authenticated or not is_moderator(user):
        raise Http404("You are not allowed to view this page")
    if request.method == "POST":
        if "Fetch" in request.POST:
            username, foss, status = fetch_user()
            #return HttpResponse(request.user)
            detail_list = zip(username, foss, status)
            context = {'detail_list' : detail_list}
            #return redirect("/mim/fetched/")
            return render_to_response('mim/fetch.html', context, context_instance=RequestContext(request))
        elif "Result" in request.POST:
            username, foss = fetch_user_result()
            detail_list = zip(username, foss)
            context = {}
            quiz_marks = []
            for (username, fos) in detail_list:
                # user must be an object of class django.contrib.auth.models.User
                user = User.objects.get(username=username)
                papers = AnswerPaper.objects.filter(user=user)
                for paper in papers:
                    marks_obtained = paper.get_total_marks()
                    max_marks = paper.question_paper.total_marks
                    percentage = round((marks_obtained/max_marks)*100,2)
                    temp = user, fos, paper.question_paper.quiz.description,\
                           marks_obtained, max_marks, percentage
                    quiz_marks.append(temp)
                    sptu_user = SpokenTutorialDetail.objects.filter(username=username)
                    for u in sptu_user:
                        u.result = percentage
                        u.result_status = "GRADED"
                        u.save()

                    insert_moodle(user, fos, percentage)
                    context = {'papers': quiz_marks}
            return render_to_response('mim/result.html', context, context_instance=RequestContext(request))
    else:
            return my_redirect('/mim')

def result(request):
     
    return HttpResponse("result")

def log(request):
    details  = SpokenTutorialDetail.objects.filter()
    return HttpResponse(details)
    #return render_to_reponse()
