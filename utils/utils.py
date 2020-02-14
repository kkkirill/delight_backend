def create_hash(*args):
    return hash(args)


def generate_upload_path(instance, filename):
    print(instance, filename)
    return 'media/'