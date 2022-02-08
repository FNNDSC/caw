import os
import sys
from concurrent.futures import ThreadPoolExecutor
import datetime
from typing import List, Tuple, Union
import typer
from chris.client import ChrisClient
from chris.cube.files import DownloadableFile
from chris.types import CUBEUrl
import logging
from pathlib import Path


def upload(client: ChrisClient, files: List[Path], parent_folder='', upload_threads=4):

    username = client.get_username()

    if parent_folder:
        upload_folder = f'{username}/uploads/{parent_folder}/{datetime.datetime.now().isoformat()}/'
    else:
        upload_folder = f'{username}/uploads/{datetime.datetime.now().isoformat()}/'

    input_files: List[Path] = []
    for path in files:
        if path.is_file():
            input_files.append(path)
        elif path.is_dir():
            nested_files = [f for f in path.rglob('**/*') if f.is_file()]
            if len(nested_files) > 0:
                input_files.extend(nested_files)
            else:
                typer.secho(f'WARNING: input directory is empty: {path}', dim=True, err=True)
        else:
            typer.secho(f'No such file or directory: {path}', fg=typer.colors.RED, err=True)
            raise typer.Abort()

    if len(input_files) == 0:
        typer.secho(f'No input files specified.', fg=typer.colors.RED, err=True)
        raise typer.Abort()

    with typer.progressbar(label='Uploading files', length=len(input_files), file=sys.stderr) as bar:
        def upload_file(input_file: str):
            client.upload(Path(input_file), Path(upload_folder))
            bar.update(1)

        with ThreadPoolExecutor(max_workers=upload_threads) as pool:
            uploads = pool.map(upload_file, input_files)

    # check for upload errors
    for upload_result in uploads:
        logging.debug(upload_result)

    typer.secho(f'Successfully uploaded {len(input_files)} files to "{upload_folder}"', fg=typer.colors.GREEN, err=True)
    return upload_folder


def download(client: ChrisClient, url: Union[str, CUBEUrl], destination: Path, threads: 4):
    """
    Download all the files from a given ChRIS API url.
    :param client: ChRIS client
    :param url: any ChRIS file resource url, e.g.
                https://cube.chrisproject.org/api/v1/uploadedfiles/
                https://cube.chrisproject.org/api/v1/uploadedfiles/?fname=chris/uploads/today
                https://cube.chrisproject.org/api/v1/3/files/
    :param destination: folder on host where to download to
    :param threads: max number of concurrent downloads
    """
    if destination.is_file():
        typer.secho(f'Cannot download into {destination}: is a file', fg=typer.colors.RED, err=True)
        raise typer.Abort()

    def __calculate_target(remote_file: DownloadableFile) -> Tuple[Path, DownloadableFile]:
        """
        Decide on a download location for a file resource in ChRIS.
        Create the parent directory if needed.
        :param remote_file: file information from ChRIS
        :return: download location on host and that file
        """
        fname = remote_file.fname
        if fname.startswith('chris/'):
            fname = fname[6:]
        target = destination.joinpath(fname)
        os.makedirs(target.parent, exist_ok=True)
        return target, remote_file

    search = tuple(client.get_files(url))
    with typer.progressbar(search, length=len(search), label='Getting information', file=sys.stderr) as progress:
        to_download = frozenset(__calculate_target(remote_file) for remote_file in progress)

    with typer.progressbar(length=len(to_download), label='Downloading files', file=sys.stderr) as progress:
        def download_file(t: Tuple[Path, DownloadableFile]) -> int:
            """
            Download file and move the progress bar
            :param t: tuple
            :return: downloaded file size
            """
            target, remote_file = t
            remote_file.download(target)
            progress.update(1)
            return target.stat().st_size

        with ThreadPoolExecutor(max_workers=threads) as pool:
            sizes = pool.map(download_file, to_download)

    total_size = sum(sizes)
    if total_size < 2e5:
        size = f'{total_size} bytes'
    elif total_size < 2e8:
        size = f'{total_size / 1e6:.4f} MB'
    else:
        size = f'{total_size / 1e9:.4f} GB'
    typer.secho(size, fg=typer.colors.GREEN, err=True)
