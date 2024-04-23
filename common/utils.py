from rest_framework.exceptions import NotFound, PermissionDenied


def get_object(model, pk, user=None, not_found_exception=NotFound):
    try:
        if user != None:
            return model.objects.get(pk=pk, user=user)
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise not_found_exception


def check_owner(req, user):
    if user != req.user:
        raise PermissionDenied
    return True
