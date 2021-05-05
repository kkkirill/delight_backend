import pytest

from test.helpers.upload_file import FileUploaderS3


@pytest.fixture
def keys():
    file_uploader = FileUploaderS3()
    ikey = file_uploader.upload_file_to_s3('test/data/dingo.png')
    fkey = file_uploader.upload_file_to_s3('test/data/song.mp3')
    yield {'ikey': ikey, 'fkey': fkey}
    file_uploader.delete_file(ikey)
    file_uploader.delete_file(fkey)
    open('.localstack/data/recorded_api_calls.json', 'w').close()
