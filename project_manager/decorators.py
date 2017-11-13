def require_status(*statuses):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if self.status not in statuses:
                raise Exception("Cannot " + method.__name__ + "() Object " \
                                + "instance, status must be '" \
                                + ','.join(statuses) + "' current status is '"+(self.status)+"'")
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

def prohibit_status(*statuses):
    def decorator(method):
        def wrapper(self, *args, ** kwargs):
            if self.status in statuses:
                raise Exception("Cannot " + method.__name__ + "() Object " \
                                + "instance, status must not be '" \
                                + ','.join(statuses) + "' current status is '"+(self.status)+"'")
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

