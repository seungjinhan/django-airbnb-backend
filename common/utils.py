from rest_framework.exceptions import NotFound, PermissionDenied


def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise NotFound


def check_owner(req, user):
    if user != req.user:
        raise PermissionDenied
    return True
