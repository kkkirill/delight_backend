from delight.settings import MAX_FILE_SIZES


def get_filepath(instance, filename):
    return f'{instance.FILE_TYPES_PATHS[instance.type]}/{filename}'


def check_file_size(request):
    file_type = request.content_type.split('/')[0]

    return request.size <= MAX_FILE_SIZES.get(file_type, 0)

