import hashlib
from datetime import datetime

from delight.settings import MAX_FILE_SIZES


def get_filepath(instance, filename):
    generated_hash = hashlib.md5(f'{filename}-{datetime.now().isoformat()}'.encode('utf-8')).hexdigest()
    name, extension = filename.split('.')[:2]
    return f'{instance.FILE_TYPES_PATHS[instance.type]}/{name}{generated_hash[:10]}{extension}'


def check_file_size(request):
    file_type = request.content_type.split('/')[0]

    return request.size <= MAX_FILE_SIZES.get(file_type, 0)

