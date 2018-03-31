from setuptools import setup

setup(
    name='aiostorage',
    version='0.1.0',
    description='Asynchronous object storage',
    long_description='Interface for performing common object storage '
                     'operations asynchronously. The aim is to support '
                     'multiple object storage providers, e.g. Google Cloud, '
                     'Backblaze, etc.',
    author='Guy King',
    author_email='guy@zorncapital.com',
    packages=[],
    classifiers=['Development Status :: 1 - Planning'],
)

# example usage
# import aiostorage
#
# videos = ('video1.mp4', 'video2.mp4', 'video3.mp4')
# storage = aiostorage.storage(provider='gcloud', auth='auth_details')
# storage.authenticate()
# for video in videos:
#     storage.upload(video, upload_location)