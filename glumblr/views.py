#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import login as login_auth
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction
from glumblr.models import *
from glumblr.forms import *
from mimetypes import guess_type
# Create your views here.
def index(request):
    return redirect('/login/')


def login(request):
    context = {}
    # if request.user.is_authenticated:
    #     return redirect(reverse('global_stream'))
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)
    # if the method is post, get data from form
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'login.html', context)
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    print("user authenticate")
    # if user is not None:
    #     user_profile = get_object_or_404(User_profile, username=form.cleaned_data['username'])
    #     if user_profile.confirm:
    #         login_auth(request, user)
    #         return redirect(reverse('global_stream'))
    #     else:
    #         token = default_token_generator.make_token(user_profile)
    #         email_body = """Please click in the link below to verify your email address
    #                 for your account: http://%s%s""" % (
    #         request.get_host(), reverse('confirm', args=(user_profile.username, token)))
    #         send_mail(subject='Verify your email address',
    #                   message=email_body,
    #                   from_email="chenyan2@andrew.cmu.edu",
    #                   recipient_list=[user_profile.email])
    #         context['email'] = form.cleaned_data['email']
    #         context['host'] = request.get_host()
    #         context['username'] = user_profile.username
    #         context['token'] = token
    #         return render(request, 'email.html', context)
    #
    # else:
    #     context['errors'] = 'Invalid username and password'
    #     return render(request, 'login.html', context)
    if user is not None:
        login_auth(request, user)
        return redirect(reverse('global_stream'))
    else:
        context['errors'] = 'Invalid username and password'
        return render(request, 'login.html', context)

@login_required
def logout(request):
    logout_auth(request)
    return redirect('/login/')

def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],
                                    last_name= form.cleaned_data['last_name'], email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.save()
    token = default_token_generator.make_token(new_user)

    new_user_profile = User_profile(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],
                                    last_name= form.cleaned_data['last_name'], email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],token_reg=token)
    new_user_profile.save()

    email_body = """Welcome to glumblr. Please click in the link below to verify your email address and complete the registeration
        for your account: http://%s%s""" % (request.get_host(), reverse('confirm', args=(new_user.username, token)))
    send_mail(subject='Verify your email address',
              message=email_body,
              from_email="chenyan2@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    context['host'] = request.get_host()
    context['username'] = new_user.username
    context['token'] = token
    return render(request, 'email.html', context)

# @transaction.commit_on_success
def confirm_registration(request, username, token):
    confirm_user_profile = get_object_or_404(User_profile, username=username)
    confirm_user = get_object_or_404(User, username=username)
    if token != confirm_user_profile.token_reg:
        print('token error')
        raise Http404
    # confirm_user.confirm = True
    confirm_user.is_active = True
    confirm_user.save()
    login_auth(request, confirm_user)
    return redirect(reverse('global_stream'))
    # user = authenticate(username=confirm_user.username, password= confirm_user.password)
    # if user is not None:
    #     login_auth(request, user)
    #     return redirect(reverse('global_stream'))
def forget_password(request):
    context = {}
    if request.method == 'GET':
        form = ForgetPasswordForm()
        context['form'] = form
        return render(request, 'forget_password.html', context)
    form = ForgetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'forget_password.html', context)
    user_profile = get_object_or_404(User_profile, email=form.cleaned_data['email'])
    user = get_object_or_404(User, username=user_profile.username)
    token_reset = default_token_generator.make_token(user)
    print('token', token_reset)
    email_body = """We have sent an email to %s, Please click in the link below to reset password: http://%s%s""" % (
        form.cleaned_data['email'], request.get_host(), reverse('reset_password_valid', args=(user_profile.username, token_reset)))
    send_mail(subject='Reset password',
              message=email_body,
              from_email="chenyan2@andrew.cmu.edu",
              recipient_list=[user_profile.email])
    user_profile.token_reset = token_reset
    user_profile.save()
    context['email'] = user_profile.email
    context['host'] = request.get_host()
    context['username'] = user_profile.username
    context['token'] = token_reset
    return render(request, 'forgetpw_email.html', context)

def forget_password_valid(request, username, token):
    context = {}
    user_profile = get_object_or_404(User_profile, username=username)
    print(username)
    if token != user_profile.token_reset:
        print('token error')
        raise Http404

    return redirect('/forget_reset_password/' + username)

def forget_reset_password(request, username):
    user_profile = get_object_or_404(User_profile, username=username)
    user = get_object_or_404(User, username=username)
    context = {}
    context['user_profile'] = user_profile
    if request.method == 'GET':
        form = ResetPasswordForm()
        context['form'] = form
        return render(request, 'reset_password.html', context)
    form = ResetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        # return render(request, 'reset_pw.html', context)
        return render(request, 'reset_password.html', context)
    if form.cleaned_data['password1'] == user_profile.password:
        context['errors'] = 'please choose another password'
        return render(request, 'reset_password.html', context)
    user_profile.password = form.cleaned_data['password1']
    user_profile.save()
    user.set_password(form.cleaned_data['password1'])
    user.save()
    login_auth(request, user)
    return redirect('/profile/' + str(request.user.username))
    return redirect('/login/')

@login_required
def reset(request):
    context = {}
    user_profile = get_object_or_404(User_profile, username=request.user.username)
    user = get_object_or_404(User, username=request.user.username)
    token_reset = default_token_generator.make_token(user)
    email_body = """Welcome to glumblr. Please click in the link below to verify your email address and complete the registeration
            for your account: http://%s%s""" % (request.get_host(), reverse('reset_password_valid', args=(user_profile.username, token_reset)))
    send_mail(subject='Verify your email address',
              message=email_body,
              from_email="chenyan2@andrew.cmu.edu",
              recipient_list=[user_profile.email])
    user_profile.token_reset = token_reset
    print('***********here')
    print(user_profile)
    print('hh')

    context['email'] = user_profile.email
    context['host'] = request.get_host()
    context['username'] = user_profile.username
    context['token'] = token_reset
    user_profile.save()
    return render(request, 'resetpw_email.html', context)

def reset_password_valid(request, username, token):
    context = {}
    reset_user = get_object_or_404(User_profile, username=username)
    if token != reset_user.token_reset:
        print('token error')
        raise Http404
    return redirect(reverse('change_password'))

def change_password(request):
    user_profile = get_object_or_404(User_profile, username=request.user.username)
    user_tofix = get_object_or_404(User, username=request.user.username)
    context = {}
    context['user_profile'] = user_profile
    if request.method == 'GET':
        form = ResetPasswordForm()
        context['form'] = form
        return render(request, 'change_password.html', context)
    form = ResetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'change_password.html', context)
    if form.cleaned_data['password1'] == user_profile.password:
        context['errors'] = 'please choose another password'
        return render(request, 'change_password.html', context)
    user_profile.password = form.cleaned_data['password1']
    user_profile.save()
    user_tofix.set_password(form.cleaned_data['password1'])
    user_tofix.save()
    login_auth(request, user_tofix)
    return redirect('/profile/' + str(request.user.username))

@login_required
def global_stream(request):
    context = {}
    user_profile = get_object_or_404(User_profile, username=request.user.username)
    messages = Message.objects.all()
    msg_list = []
    for msg in reversed(messages):
        msg_list.append(msg)
    friends = user_profile.friends.all()

    if len(friends) > 5:
        context['friends'] = friends.reverse()[:5]
    else:
        context['friends'] = friends.reverse()
    context['user_profile'] = user_profile
    context['request'] = request

    return render(request, 'global.html', context)

@login_required
def get_global_message(request):
    print("in get_global_message")
    max_time = Message.get_max_time()
    print("max_time", max_time)
    messages = Message.get_messages()
    messages = messages.order_by('-last_changed')
    user = get_object_or_404(User_profile, id=request.user.id)
    # username = user.username
    picture = user.picture
    # print(picture)
    # # message 需要在待评论区域显示照片
    # context = {"max_time": max_time, "messages": messages, "username": username, "picture": picture}
    context = {"max_time":max_time, "messages":messages,"picture":picture}
    # print("after context")
    return render(request, 'messages.json', context, content_type='application/json')

def get_changes_global(request, time="1970-01-01T00:00+00:00"):
    max_time = Message.get_max_time()
    messages = Message.get_changes(time)
    # messages = messages.order_by('last_changed')
    user = get_object_or_404(User_profile, id=request.user.id)
    picture = user.picture
    context={"max_time": max_time, "messages":messages, "picture":picture}

    return render(request, 'messages.json', context, content_type='application/json')


# 同时有两个参数？
def get_profile_message(request, username):
    print("in get_profile_message")
    max_time = Message.get_max_time()
    messages_1 = Message.get_messages()
    messages_1 = messages_1.order_by('last_changed')
    messages_2 = Message.objects.filter(user_profile__username=username)
    messages = []
    for message in messages_1:
        if message in messages_2:
            messages.append(message)
    user = get_object_or_404(User_profile, id=request.user.id)
    picture = user.picture
    context = {"max_time":max_time, "messages":messages, "picture":picture}
    return render(request, 'messages.json', context, content_type='application/json')

def get_changes_profile(request, username, time="1970-01-01T00:00+00:00"):
    max_time = Message.get_max_time()
    messages_1 = Message.get_changes(time)
    # messages_1 = messages_1.order_by('last_changed')
    messages_2 = Message.objects.filter(user_profile__username=username)
    # messages = []
    # list(set(listA).intersection(set(listB)))
    messages = list(set(messages_1).intersection(set(messages_2)))
    user = get_object_or_404(User_profile, id=request.user.id)
    picture = user.picture
    context = {"max_time":max_time, "messages":messages, "picture":picture}
    return render(request, 'messages.json', context, content_type='application/json')

@login_required
def profile(request, username):
    # user_id is the user's home page that you want to visit
    context = {}
    # when the owner post message
    if request.method == 'POST':
        user_profile = get_object_or_404(User_profile, username=request.user.username)
         # if user only press "post" button but did not enter any message, it will not show any record.
        form = MessageForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'profile.html', context)

    if request.method == 'GET' and username == request.user.username:
        form = MessageForm()
        context['form'] = form
    user_profile = get_object_or_404(User_profile, username=username)
    friends = user_profile.friends.all()

    if len(friends) > 5:
        context['friends'] = friends.reverse()[:5]
    else:
        context['friends'] = friends.reverse()
    context['user_profile'] = user_profile
    context['request'] = request
    # to detect if this person is followed by the user
    if request.user.username != user_profile.username:
        owner_profile = get_object_or_404(User_profile, username=request.user.username)
        owner_friends = owner_profile.friends.all()
        owner_friends_name = []
        for owner_friend in owner_friends:
            owner_friends_name.append(owner_friend.username)
        if username in owner_friends_name:
            print('already followed')
            context['unfollow'] = 'Unfollow'
        else:
            print('have not followed')
            context['follow'] = 'Follow'
    return render(request, 'profile.html', context)


def post_message(request):
    print("in views.py post_message")
    if not 'message' in request.POST or not request.POST['message']:
        raise Http404
    else:
        if len(request.POST['message']) > 42:
            # context = {"errors": "The message should be no longer than 42 characters."}
            return redirect('/profile/' + str(request.user.username))

        # user_profile = User_profile.objects.get(id=request.user.id)
        user_profile = get_object_or_404(User_profile, username=request.user.username)

        new_message = Message(content=request.POST['message'],user_profile=user_profile)
        new_message.save()
    return HttpResponse("")

def delete_message(request, id):
    try:
        message_to_delete = Message.objects.get(id=id)
        message_to_delete.deleted = True
        message_to_delete.save()
    except ObjectDoesNotExist:
        return HttpResponse("The message did not exist")
    return HttpResponse("")


@login_required
def follow_stream(request, username):
    context = {}
    context['request'] = request
    # owner_profile = get_object_or_404(User_profile, username=request.user.username)
    user_profile = get_object_or_404(User_profile, username=username)
    friends = user_profile.friends.all()
    friends_list = []
    # message_list = []
    for friend in reversed(friends):
        friends_list.append(friend)
        # message = Message.objects.filter(user_profile = friend)
        # message_list.extend(message)
        # message_list.extend(get_object_or_404(Message, user_profile=friend))
    message_list = Message.objects.filter(user_profile__in=friends).order_by('-last_changed')
    # print('*********************')
    # print(message_list)
    # message_list = message_list.order_by('-last-changed')
    message_list_new = []
    # for message
    context['friends'] = friends_list
    context['user_profile'] = user_profile
    context['message_list'] = message_list
    return render(request, 'follow_stream.html', context)


@login_required
def edit(request):
    context = {}
    profile_to_edit = get_object_or_404(User_profile, username=request.user.username)
    # get method lead to the form page
    if request.method == 'GET':
        # user_profile = User_profile.objects.get(user=request.user)
        form = User_profileForm(instance=profile_to_edit)
        context['form'] = form
        context['user_profile'] = profile_to_edit
        return render(request, 'edit_profile.html', context)

    # post method retrieve the input from user, and add value in html can save previous result.
    form = User_profileForm(request.POST, request.FILES, instance=profile_to_edit)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'edit_profile.html', context)
    form.save()
    return redirect('/profile/' + str(request.user.username))


# @login_required
def delete(request, id):
    context = {}
    try:
        d_msg = Message.objects.get(id=id)
        d_msg.delete()
    except ObjectDoesNotExist:
        context['errors'] = 'The message is not in the post history'

    return redirect('/profile/' + str(request.user.username))


@login_required
def follow(request, username):
    # context = {}
    profile_to_edit = get_object_or_404(User_profile, username=request.user.username)
    friends_to_add = get_object_or_404(User_profile, username=username)
    profile_to_edit.friends.add(friends_to_add)
    profile_to_edit.save()
    return redirect('/profile/' + str(username))

@login_required
def unfollow(request, username):
    profile_to_edit = get_object_or_404(User_profile, username=request.user.username)
    friends_to_delete = get_object_or_404(User_profile, username=username)
    profile_to_edit.friends.remove(friends_to_delete)
    # profile_to_edit.save()
    return redirect('/profile/' + str(username))


def get_comments(request, id):
    print("get_comments. view.py")
    message = get_object_or_404(Message, id=id)
    print("message get")
    # comments = get_object_or_404(Comment, message=message)
    comments = Comment.objects.filter(message=message)

    context = {'comments':comments, 'id':id}
    # return HttpResponse("")
    return render(request, 'comments.json', context, content_type='application/json')


def post_comment(request, id):
    if not 'comment' in request.POST:
        print("no key in request.POST")
        raise Http404
    elif not request.POST['comment']:
        print('not request.POST comment')
        raise Http404
    # elif request.POST
    else:
        if len(request.POST['comment']) > 42:
            return HttpResponse("")
        print("in post_comment")
        message=get_object_or_404(Message,id=id)
        user_profile = get_object_or_404(User_profile, id=request.user.id)
        new_comment = Comment(content=request.POST['comment'], message=message, user_profile=user_profile)
        new_comment.save()
        return HttpResponse("")

@login_required
def get_photo(request, username):
    user_profile = get_object_or_404(User_profile, username=username)
    if not user_profile.picture:
        raise Http404

    content_type = guess_type(user_profile.picture.name)
    return HttpResponse(user_profile.picture, content_type=content_type)
