import requests
import io

from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector

from celery import shared_task, task
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from transliterate import translit

from invoices.util import get_pdf_generator_url
from invoices.models import Invoice
from core.models import CredentialsModel

class GoogleAuthDjango(GoogleAuth):

    def LoadCredentialsDjango(self, user_id=None):
        """Loads credentials or create empty credentials if it doesn't exist.
        Loads credentials file from path in settings if not specified.
        :param credentials_file: path of credentials file to read.
        :type credentials_file: str.
        :raises: InvalidConfigError, InvalidCredentialsError
        """
        storage = DjangoORMStorage(CredentialsModel, 'id', User.objects.get(id=user_id), 'credential')
        self.credentials = storage.get()


class GoogleDriveFileBinary(GoogleDriveFile):

    # def __init__(self, settings_file='settings.yaml',http_timeout=None):
    #     super().__init__(settings_file, http_timeout)
    #     self.settings['get_refresh_token'] = True

    def SetContentFileBinary(self, content):
        self.content = io.BytesIO(content)


@shared_task
def save_invoice_to_google_drive(user_id, settings):
    if 'gdrive_sync' not in settings or not settings['gdrive_sync']:
        print('Google drive sync not enabled for user_id=' + str(user_id))
        return
    if 'gdrive_folder' not in settings or not settings['gdrive_folder']:
        settings['gdrive_folder'] = 'webinvoices.eu'
    if 'filename' not in settings:
            raise Exception("You must provide 'filename' key in settings")
    if 'invoice_id' not in settings:
            raise Exception("You must provide 'invoice_id' key in settings")
    #print('PDF export TASK')
    settings['filename'] = translit(settings['filename'], 'bg', reversed=True)
    gauth = GoogleAuthDjango()
    gauth.LoadCredentialsDjango(user_id)
    if gauth.access_token_expired:
        gauth.Refresh()
    drive = GoogleDrive(gauth)

    flist = drive.ListFile({
        'q': "title = '{}' and trashed = false".format(settings['gdrive_folder'])
    })
    found_dirs = flist.GetList()
    if len(found_dirs) == 0:
        # Create folder.
        folder_metadata = {
            'title': settings['gdrive_folder'],
            # The mimetype defines this new file as a folder, so don't change this.
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
    else:
        folder = found_dirs[0]

    flist = drive.ListFile({
        'q': "title = '{}' and trashed = false and '{}' in parents".format(settings['filename'], folder.metadata['id'])
    })
    found_files = flist.GetList()
    # print(found_files)
    if len(found_files) == 0:
        metadata = {
            'parents': [{"kind": 'drive#fileLink', 'id': folder['id']}],
            'title': settings['filename'],
            'mimeType': 'application/pdf',
            # 'properties': [{
            #     'key':'webinvoicesID',
            #     'value': settings['invoice_id'],
            #     'visibility': 'PUBLIC',
            # }]
        }
    else:
        metadata = {
            'id': found_files[0].metadata['id']
        }

    # Upload file to folder.
    f = GoogleDriveFileBinary(auth=drive.auth, metadata=metadata)

    pdf_generator_url = get_pdf_generator_url(settings['invoice_id'])
    r = requests.get(pdf_generator_url)

    # Make sure to add the path to the file to upload below.
    f.SetContentFileBinary(r.content)
    f.Upload()
    #print('Export PDF Done!')


@task
def update_search_vector():
    vector= SearchVector('client_name') + SearchVector('client_city') + SearchVector('client_mol') +\
        SearchVector('client_address')

    for inv in Invoice.objects.annotate(document=vector):
        inv.search_vector = inv.document
        inv.save(update_fields=['search_vector'])
