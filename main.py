import json
import os
import tempfile

from google.cloud import storage
from wand.color import Color
from wand.image import Image

storage_client = storage.Client()

with open('config.json') as f:
    config = json.loads(f.read())


def handle_message(data, context):
    blob = storage_client.bucket(data['bucket']).get_blob(data['name'])
    output_bucket = storage_client.bucket(config['output_bucket'])
    write_thumbnails(blob, output_bucket)


def write_thumbnails(blob, output_bucket):
    _, temp_doc_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_doc_filename)
    print(f'Image {blob.name} was downloaded to {temp_doc_filename}.')

    # Generate thumbnail images for each page of the doc and upload to GCS
    doc = Image(filename=temp_doc_filename, resolution=config['resolution'])
    for i, page in enumerate(doc.sequence):
        for size in config['thumbnail_sizes']:
            with Image(page) as image:
                image.format = 'png'
                image.background_color = Color('white')
                image.alpha_channel = 'remove'
                image.transform(resize='{}x{}'.format(size, size))
                _, temp_image_filename = tempfile.mkstemp()
                image.save(filename=temp_image_filename)

                image_blob_name = f'{blob.name}/{size}/{i + 1}.png'
                image_blob = output_bucket.blob(image_blob_name)
                image_blob.metadata = {'source_uri': f'gs://{blob.bucket}/{blob.name}'}
                image_blob.upload_from_filename(temp_image_filename)
                print(f'Uploaded thumbnail image gs://{output_bucket.name}/{image_blob_name}.')
                os.remove(temp_image_filename)

    # Delete the temporary document file
    os.remove(temp_doc_filename)
