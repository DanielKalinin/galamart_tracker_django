from django.contrib.contenttypes.models import ContentType

TAGGED_MODELS = [
    'work',
    'resource',
    'container',
    'requirement'
]

def get_by_tag(project, tag):
    found_one = False
    for model_name in TAGGED_MODELS:
        model = ContentType.objects.get(model=model_name).model_class()
        try:
            instance = model.objects.get(project=project, tag=tag)
        except model.DoesNotExist:
            pass
        else:
            if found_one:
                raise Exception("More than one instance with same name found")
            found_one = True
    if not found_one:
        raise Exception("Instance not found")
    return instance


def get_by_tag_list(project, tag_list):
    objects = []
    for tag in tag_list:
        objects.append(get_by_tag(tag))
    return objects

