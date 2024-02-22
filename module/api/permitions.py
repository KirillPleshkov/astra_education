from rest_framework import permissions


class IsOwnerStudent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user_disciplines = request.user.curriculum.disciplines.all()
        user_modules = [list(discipline.modules.all()) for discipline in user_disciplines]
        user_modules_normal = [item for sublist in user_modules for item in sublist]

        return obj in user_modules_normal
