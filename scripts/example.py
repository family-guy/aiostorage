import os

import aiostorage

video_dir = os.path.join('tests', 'data', 'videos')
video_files = (
    'Helene Fischer - Atemlos durch die Nacht.mp4',
    'Luis Fonsi - Despacito ft Daddy Yankee.mp4',
    'Rino Gaetano - Ma il cielo è sempre più blu.webm',
    'Stromae - Alors On Danse.webm',
)
content_type = 'video/mp4'
videos = [
    {
        'path': os.path.join(video_dir, video_file),
        'content_type': content_type
    } for video_file in video_files
]

provider = 'backblaze'
credentials = {
    'account_id': os.environ['BACKBLAZE_ACCOUNT_ID'],
    'app_key': os.environ['BACKBLAZE_APP_KEY'],
}
storage = aiostorage.BlobStorage(provider, credentials)
storage.upload_files(os.environ['BACKBLAZE_TEST_BUCKET_ID'], videos)
