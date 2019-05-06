from pkdb_app.users.models import PUBLIC
from rest_framework import permissions

def is_allowed_method(request):
    allowed_methods = ["PUT",*permissions.SAFE_METHODS]
    if request.method in allowed_methods :
        return True
    return False

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user

class IsAdminOrCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if is_allowed_method(request):
            return True

        user = request.user
        return user.is_staff or (user == obj.creator)




class IsAdminOrCreatorOrCurator(permissions.BasePermission):
    """
    for study and reference
    """

    def has_object_permission(self, request, view, obj):

        if is_allowed_method(request):
            return True

        # for reference model
        if obj.study.first():
            allowed_user = (request.user == obj.study.first().creator) or (request.user in obj.study.first().curators.all())
        else:
            allowed_user = True


        return request.user.is_staff or allowed_user

class StudyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return study_permissions(request,obj)


def study_permissions(request, obj):
    study_permissions = {"admin": admin_permission(),
                         "basic": basic_permission(request, obj),
                         "reviewer": reviewer_permission(request,obj),
                         "anonymous": anonymous_permissions(request, obj)}


    return study_permissions[user_group(request)]

def user_group(request):

    try:
        user_group = request.user.groups.first().name
    except AttributeError:

        if request.user.is_superuser:
            user_group = "admin"

        else:
            user_group = "anonymous"

    return user_group

def get_study_permission(user,obj):
    allowed_user_modify = (user == obj.creator) or (user in obj.curators.all())
    allow_user_get =(user in obj.collaborators.all()) or  (obj.access == PUBLIC) or allowed_user_modify

    return {
        "admin": True,
        "anonymous":(obj.access == PUBLIC),
        "reviewer": True,
        "basic": allow_user_get
     }



def anonymous_permissions(request,obj):
    if is_allowed_method(request):
        return get_study_permission(request.user, obj)
    return False


def basic_permission(request, obj):

    user = request.user
    allowed_user_modify = (user == obj.creator) or (user in obj.curators.all())

    if is_allowed_method(request):
        return get_study_permission(user, obj)


    return allowed_user_modify


def reviewer_permission(request,obj):

    if is_allowed_method(request):
        return get_study_permission(request.user, obj)
    else:
        return False


def admin_permission():
    return True



