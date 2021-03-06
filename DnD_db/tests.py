from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

from .models import *


# Create your tests here.

def has_free_player(user):
    if isinstance(user, AnonymousUser):
        return False
    return not all([p.session_part for p in get_free_players(user.profile)])


def get_free_players(profile):
    return get_any_free_pl(profile).exclude(character=None)


def get_any_free_pl(profile):
    p_list = Player.objects.filter(user=profile).exclude(session_part__in=Session.objects.all())
    session_leaders = Session.objects.values_list('author_id')
    return p_list.exclude(id__in=session_leaders)  # Exclude session leaders


def can_delete_object(func):
    """
    Tests if current user can delete object, by comparison with object author
    :param func: wrapped
    :return: wrapped function or error
    """

    def wrapper(*args, **kwargs):
        profile = args[0].user.profile
        obj = get_object_or_404(kwargs['model'], id=kwargs['id'])
        if "author_id" in obj.__dict__.keys():
            owner_player = Player.objects.get(id=obj.author_id)
        else:
            owner_player = obj  # Object is Player model instance
        if owner_player.user_id != profile.id:
            return HttpResponseNotFound("<h1>You have no permission to do that</h1>")
        return func(*args, **kwargs)

    return wrapper


def can_edit_object(profile, user_profile):
    return profile == user_profile


def is_author(func):
    """
    Tests if current user is this session leader
    :param func: wrapped
    :return: wrapped function or error
    """

    def wrapper(*args, **kwargs):
        profile = args[0].user.profile
        sess = get_object_or_404(Session, id=kwargs['sess_id'])
        if not Player.objects.filter(user=profile).filter(id=sess.author_id).exists():
            return HttpResponseNotFound("<h1>You can not do this</h1>")
        return func(*args, **kwargs)

    return wrapper
