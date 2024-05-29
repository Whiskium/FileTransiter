import datetime
import os
import pytz
import re
import requests

from urllib.parse import unquote

def get_file_name(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}
    file_requests = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    if file_requests.ok:
        content_disposition = file_requests.headers.get('content-disposition')
        filename = False
        if content_disposition:
            content_disposition_set = content_disposition.split(';')
            for span in content_disposition_set:
                if span.strip().startswith('filename='):
                    filename = span.split('filename=')[-1].strip(' "\'')
        if not filename and os.path.basename(file_requests.url):
            filename = os.path.basename(file_requests.url).split('?')[0]
        if not filename:
            return datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
        filename = os.path.basename(unquote(filename.encode('unicode_escape').decode('utf-8').replace('\\x', '%')))
        return filename
    else:
        raise Exception('Failed to request.')

if __name__ == '__main__':
    DL_URL = os.environ.get('DL_URL')
    FILE_NAME = get_file_name(DL_URL)
    ARTIFACT_NAME = re.sub(r'[\"\[\]\<\>\{\}\|\%\\\^\`\,\(\)\— ]+', '', FILE_NAME)
    print(f'\033[34mMessage: [File Name] {FILE_NAME}\033[0m')
    print(f'\033[34mMessage: [Artifact Name] {ARTIFACT_NAME}.zip\033[0m')
    os.system('echo "FILE_NAME=%s" >> $GITHUB_OUTPUT' % FILE_NAME)
    os.system('echo "ARTIFACT_NAME=%s" >> $GITHUB_OUTPUT' % ARTIFACT_NAME)
