from django.shortcuts import render, redirect
import logging
from .models import User, Messages, Group
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

logging.basicConfig(filename='jinja.log', encoding='utf-8', level=logging.ERROR,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


def chat(request):
    return render(request, 'chat/room.html', {'room_name': "", 'user': request.user.username})


def room(request, room_name):
    group = Group.objects.filter(group_name=room_name).first()
    messages = Messages.objects.filter(group=group.id)
    return render(request, 'chat/room.html', {'room_name': group.group_name, 'user': request.user.username, 'messages': messages})


class UserRegistration(View):

    def post(self, request):
        """
        This method add the user to the database
        """
        try:
            User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'),
                                     first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'),
                                     email=request.POST.get('email'), phone=request.POST.get('phone'),
                                     location=request.POST.get('location'))
            return redirect('login')
        except Exception as ex:
            logger.exception(ex)
            return render(request, 'chat/registration.html')

    def get(self, request):
        return render(request, 'chat/registration.html')


class UserLogin(View):
    """
    This class check the user in the database
    """
    template_name = 'chat/login.html'

    def post(self, request):
        """
        This method use to log in the user
        """
        try:
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
                return redirect('get_group')
            return render(request, self.template_name)
        except Exception as ex:
            logger.exception(ex)
            return render(request, self.template_name)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('get_group')
        return render(request, self.template_name)


class UserLogout(View):
    """
    This class logout the user from profile page
    """
    def get(self, request):
        logout(request)
        return redirect('login')



def post_group(request):
    try:
        if request.method == 'GET':
            return render(request, 'chat/create_group.html')
        if request.method == 'POST':
            Group.objects.create(group_name=request.POST.get('group_name'), user=request.user)
            return redirect('get_group')
    except Exception as ex:
        logger.exception(ex)
        return render(request, "chat/create_group.html")

def get_group(request):
    try:
        if request.method == 'GET':
            groups = Group.objects.filter(user=request.user).order_by('id')
            return render(request, "chat/index.html", {'groups': groups})
    except Exception as ex:
        logger.exception(ex)
        return render(request, "chat/index.html")

def put_group(request, id):
    try:
        group = Group.objects.get(id=id, user=request.user)
        if request.method == 'GET':
            return render(request, 'chat/update_group.html', {'group': group})
        if request.method == 'POST':
            group.group_name = request.POST.get('group_name')
            group.save()
            return redirect('get_group')
    except Exception as ex:
        logger.exception(ex)
        return render(request, "chat/update_group.html")

def delete_group(request, id):
    try:
        group = Group.objects.get(id=id, user=request.user)
        group.delete()
        return redirect('get_group')
    except Exception as ex:
        logger.exception(ex)
        return render(request, "chat/index.html")


def add_members(request, group_id=None, user_id=None):
    try:
        users = User.objects.all().exclude(id=request.user.id)
        group = Group.objects.get(id=group_id, user=request.user)
        if request.method == 'GET':
            return render(request, 'chat/add_member.html', {'users': users, 'group': group})
        if request.method == 'POST':
            user = User.objects.get(id=user_id)
            user_list = group.members.filter(id=user_id)
            if user not in user_list:
                group.members.add(user)
                group.save()
                # return redirect('get_group')
                return render(request, 'chat/add_member.html', {'users': users, 'group': group})
            messages.info(request, "User already added to the group")
            return render(request, 'chat/add_member.html', {'users': users, 'group': group})
    except Exception as ex:
        logger.exception(ex)
        return render(request, 'chat/add_member.html')

def get_members(request, id):
    try:
        if request.method == 'GET':
            group = Group.objects.get(id=id, user=request.user)
            members = group.members.all()
            return render(request, "chat/view_member.html", context={'members': members, 'group': group})
    except Exception as ex:
        logger.exception(ex)
        # return render(request, "chat/view_member.html")
        return render(request, "chat/index.html")


def delete_members(request, group_id=None, user_id=None):
    try:
        group = Group.objects.get(id=group_id, user=request.user)
        user = User.objects.get(id=user_id)
        group.members.remove(user)
        return redirect('get_members', group_id)
    except Exception as ex:
        logger.exception(ex)
        return redirect('get_members')

