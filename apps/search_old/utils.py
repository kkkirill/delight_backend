from django.core.management import call_command


def rebuild_elasticsearch_index():
    call_command('search_index', '--rebuild', '-f')


def delete_elasticsearch_index():
    call_command('search_index', '--delete', '-f')
