from concurrent.futures import ThreadPoolExecutor
import datetime
from typing import List
import typer
from chrisclient2.chrisclient import ChrisClient
import logging
from pathlib import Path


def upload(client: ChrisClient, files: List[Path], parent_folder='', upload_threads=4):

    if parent_folder:
        upload_folder = f'chris/uploads/{parent_folder}/{datetime.datetime.now().isoformat()}/'
    else:
        upload_folder = f'chris/uploads/{datetime.datetime.now().isoformat()}/'

    input_files = []
    for mri in files:
        if mri.is_file():
            input_files.append(mri)
        elif mri.is_dir():
            if len(files) != 1:
                typer.secho(f'WARNING: contents of {mri} will be uploaded to the top-level, '
                            'i.e. directory structure is not preserved.', dim=True, err=True)
            input_files += [f.absolute().name for f in mri.rglob('*')]
        else:
            typer.secho(f'No such file or directory: {mri}', fg=typer.colors.RED, err=True)
            raise typer.Abort()

    with typer.progressbar(label='Uploading files', length=len(input_files)) as bar:
        def upload_file(input_file: str):
            client.upload(input_file, upload_folder)
            bar.update(1)

        with ThreadPoolExecutor(max_workers=upload_threads) as pool:
            uploads = pool.map(upload_file, input_files)

    # check for upload errors
    for upload_result in uploads:
        logging.debug(upload_result)

    typer.secho(f'Successfully uploaded {len(input_files)} files to "{upload_folder}"', fg=typer.colors.GREEN, err=True)
    return upload_folder
