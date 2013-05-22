from django.core.validators import email_re
import sys
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pro.settings import MEDIA_URL
from crow.models import item,profile,tag
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from django.shortcuts import render
from crow.models import profile
from django.core.context_processors import csrf

from django.db import IntegrityError
from django.template import RequestContext
from django.contrib.auth.models import User
from cStringIO import StringIO
import Image
from PIL import Image
  

#
import base64
from crow.forms import uploadImageForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.contrib.auth import logout
from crow.forms import ProfileForm
#import re




# deals with single image links
def viewSingleItem(request,reqId):
    #do something to clear the name string. refer appengine
    reqId=escape(reqId)
    currItem=get_object_or_404(item,id=reqId)
    user=request.user
    return render_to_response('site/singleImage.html',{'item':currItem,'user':user})

def viewLoginAddonImage(request):
    if (request.method =='POST'):
        username=escape(request.POST['username'])
        password=escape(request.POST['password'])   #do it with django forms
        user=authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/imagesubmit/')
                
            else:
                pass
                # Return a 'disabled account' error message
    else:
        return render_to_response('site/login.html',context_instance=RequestContext(request))

    
def viewLoginAddonVideo(request):
    if (request.method =='POST'):
        username=escape(request.POST['username'])
        password=escape(request.POST['password'])   #do it with django forms
        user=authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/videosubmit/')
                
            else:
                pass
                # Return a 'disabled account' error message
    else:
        return render_to_response('site/login.html',context_instance=RequestContext(request))

def viewLoginError(request):
    return HttpResponse("Login Error")

@csrf_exempt
@login_required(login_url='/app-login1')
def viewSubmitImage(request):
    if request.method=='POST':
        if request.POST.get('file') and request.POST.get('url'):
            img=base64.b64decode(request.POST.get('file'))
        else:
            return HttpResponse(" conversion failed ");
        form=uploadImageForm(request.POST)
        if form.is_valid():
            image=item(
                text=form.cleaned_data["text"],
                url=form.cleaned_data["url"],
                user=request.user,
                isImage=True,)
            
            image.image.save("img.jpeg",ContentFile(img),save=True)
            image.save()
            getTags(form.cleaned_data["text"],theItem=image,theUser=request.user)
            return HttpResponse("Thank you") #say thank you
    else:    
        return render_to_response('site/clip.html',context_instance=RequestContext(request))




@csrf_exempt
@login_required(login_url='/app-login2')
def viewSubmitVideo(request):
    if request.method=='POST':
        if request.POST.get('url'):
            form=uploadImageForm(request.POST)
            if form.is_valid():
                vid=item(
                     text=form.cleaned_data["text"],
                     url=form.cleaned_data["url"],
                     user=request.user,
                     isVideo=True,)
                vid.save()
                getTags(form.cleaned_data["text"],theItem=vid,theUser=request.user)
                return HttpResponse("Thank you")
            else:
                return HttpResponse(" Tampered form")
    else:
        return render_to_response('site/clip2.html',context_instance=RequestContext(request))
    
    


def viewLogoutAddon(request):
    logout(request)
    return redirect("/")

@login_required
def viewMyFeed(request):
    if request.method=='POST':
        rtext=request.POST.get("shout_input")
        newItem=item(text=rtext,user=request.user)
        newItem.isText=True
        newItem.save()
        getTags(rtext,theItem=newItem,theUser=request.user)
        return redirect("/myfeed/")
    
    theUser=request.user
    try:
        followList=profile.objects.get(user=theUser).following.all()
        itemList=[]
        try:
            for i in followList:
                 itemList.append(item.objects.filter(user=i).order_by('-date'))
            itemList=itemList[0]
            paginator=Paginator(itemList,10)
            page=request.GET.get('page')
            try:
                itemPage=paginator.page(page)
            except PageNotAnInteger:
                itemPage=paginator.page(1)
            except EmptyPage:
                itemPage=paginator.page(paginator.num_pages)
        except:
            itemPage=False   #Give a nice message saying you havent followed any users
    except profile.DoesNotExist:
        itemPage=False   #set profile along with user Login
          
    return render_to_response("site/myfeed.html", {"path":request.get_full_path,"user":theUser,'itempage':itemPage},context_instance=RequestContext(request))
    




def getTags(text,theItem,theUser):
    
    tags= set(part[1:] for part in text.split() if part.startswith('#'))
    for i in tags:
        try:
           t= tag.objects.get(tagname=i)
           t.items.add(theItem)
           t.users.add(theUser)
        except tag.DoesNotExist :
            newTag=tag(tagname=i )
            newTag.save()
            newTag.items.add(theItem)
            newTag.users.add(theUser)

def viewTag(request,theTag):
    itemList=tag.objects.get(tagname=theTag).items.all()
    paginator=Paginator(itemList,10)
    page=request.GET.get('page')
    try:
        itemPage=paginator.page(page)
    except PageNotAnInteger:
        itemPage=paginator.page(1)
    except EmptyPage:
        itemPage=paginator.page(paginator.num_pages)

    return render_to_response("site/myfeed.html", {"isMyFeed":True,"viewTag":True,"user":request.user,'itempage':itemPage},context_instance=RequestContext(request))
    
def viewProfile(request,userId):
    theUser=User.objects.get(username=userId)
    userProfile=profile.objects.get(user=theUser)
    followerCount=userProfile.followers.all().count()
    followingCount=userProfile.following.all().count()
    itemList=item.objects.filter(user=theUser).order_by('-date')
    shoutCount=itemList.count()

    #followerview = []
    #followingview=[]
    #for followerss in profile.objects.all():
     #   followerdict = {}
      #  followerdict['follower_object'] = followerss
       # followerview.append(followerdict)
    follower=profile.objects.all()
    
    paginator=Paginator(itemList,10)
    page=request.GET.get('page')
    try:
        itemPage=paginator.page(page)
    except PageNotAnInteger:
        itemPage=paginator.page(1)
    except EmptyPage:
        itemPage=paginator.page(paginator.num_pages)

    return render_to_response("site/profile.html", {"viewTag":True,"currUser":request.user,'theUser':theUser,'userProfile':userProfile,"followerCount":followerCount,"followingCount":followingCount,"shoutCount":shoutCount,'itempage':itemPage,"follower":follower},context_instance=RequestContext(request))
    
@login_required
@csrf_exempt
def viewFollowBtn(request):
    if request.method=="POST":
        currUser=request.user
        if currUser.is_authenticated():
            userId=request.POST.get("userId")
            currProfile=profile.objects.get(user=currUser)
            currProfile.following.add(User.objects.get(username=userId))
            return redirect('/users/'+userId)
    else:
        return HttpResponse(" Bad request")

@csrf_exempt
def viewTrending(request):
    itemList=item.objects.all().order_by("-date")
    paginator=Paginator(itemList,10)
    page=request.GET.get('page')
    try:
        itemPage=paginator.page(page)
    except PageNotAnInteger:
        itemPage=paginator.page(1)
    except EmptyPage:
        itemPage=paginator.page(paginator.num_pages)

    return render_to_response("site/myfeed.html", {"isTrending":True,"viewTag":True,"user":request.user,'itempage':itemPage},context_instance=RequestContext(request))
"""
@csrf_exempt

def viewProfileEdit(request,userId):
    c = {}
    c.update(csrf(request))
    des = request.POST["description"]
    try:
        list=profile.objects.get(description=des)
        list.description=des
    except profile.DoesNotExist:
        
        list=profile(user=request.user ,description=des)
    list.save()
    return HttpResponse("helllooo")
"""
    
@csrf_exempt
def edit_profile(request, username, form_class=None, template_name='site/edit_profile.html',
                 extra_context=None):
    success_url=None
    
    user = get_object_or_404(User, username=username)
    
    

    #user = request.user
    profile_obj = user.get_profile()
    #if request.user.is_authenticated():
        #user=request.user.get_profile
    if success_url is None:
        success_url = reverse('crow.views.viewProfile',args=(request.user.username,))
    #if ProfileForm is None:
        #ProfileForm = utils.get_profile_form()
    theUser=User.objects.get(username=username)
    userProfile=profile.objects.get(user=theUser)
    
    if request.method == 'POST':
        userprofile_edit = ProfileForm(request.POST, request.FILES, instance = request.user.get_profile())
        if userprofile_edit.is_valid():
            
            userprofile_edit.save()
            return HttpResponseRedirect(success_url)
            #return HttpResponse("thank u")
            #if 'img' in request.FILES:
                #imgage=Image.open(form.cleaned_data['img']
            

        else:
            return render_to_response('site/test.html', { 'form': userprofile_edit,
                                'profile': profile_obj, },
                              context_instance=RequestContext(request))
    else:
        userprofile_edit = ProfileForm(None)
        #userprofile_edit = ProfileForm(instance = request.user.get_profile())
        #return HttpResponse("thank u")

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': userprofile_edit,
                                'profile': profile_obj, },
                              context_instance=RequestContext(request))
edit_profile = login_required(edit_profile)



@csrf_exempt
def resize_uploaded_image1(buf):
    

    image = Image.open(buf)

    maxSize = (33, 33)
    resizedImage = image.thumbnail(maxSize, Image.ANTIALIAS)

    # Turn back into file-like object
    resizedImageFile = StringIO()
    resizedImage.save(resizedImageFile , 'PNG', optimize = True)
    resizedImageFile.seek(0)    # So that the next read starts at the beginning

    return resizedImageFile

"""

@csrf_exempt
            image = request.FILES['profilepic']
            resizedImage = resize_uploaded_image(image)
            content = django.core.files.File(resizedImage)
            acc = profile.objects.get(user=request.user)
            acc.small.save(image.name, content)
def resize_uploaded_image(buf):
    #image = Image.open(buf)
    imagefile  = StringIO(buf.read())
    imageImage = Image.open(imagefile)


    (width, height) = imageImage.size
    (width, height) = scale_dimensions(width, height, longest_side=240)

    resizedImage = imageImage.resize((width, height))

    # Turn back into file-like object
    resizedImageFile = StringIO.StringIO()
    resizedImage.save(resizedImageFile , 'JPEG')
    
    resizedImageFile.seek(0)    # So that the next read starts at the beginning

    return resizedImageFile
"""


@csrf_exempt
def viewEdit(request,userId):
    return render(request, 'edit_profile.html')


      

#paginate item list
    #follow button
    #render template
    
    
