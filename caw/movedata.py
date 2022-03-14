import datetime
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Tuple, Union

import requests
import typer

from chris.client import ChrisClient
from chris.cube.files import DownloadableFile
from chris.cube.pagination import TooMuchPaginationException, MAX_REQUESTS, REQUESTS_ENV_VAR_NAME
from chris.types import CUBEUrl


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

    files_to_download = _discover_files_to_download(client, url)

    with typer.progressbar(files_to_download, length=len(files_to_download), label='Getting information', file=sys.stderr) as progress:
        to_download = frozenset(__calculate_target(remote_file) for remote_file in progress)

    with typer.progressbar(length=len(to_download), label='Downloading files', file=sys.stderr) as progress:
        with ThreadPoolExecutor(max_workers=threads) as pool:

            def download_file(t: Tuple[Path, DownloadableFile]) -> int:
                """
                Download file and move the progress bar
                :return: downloaded file size
                """
                target, remote_file = t
                try:
                    remote_file.download(target)
                except requests.exceptions.RequestException as e:
                    typer.secho(f'Failed to download {remote_file.file_resource}: {str(e)}',
                                fg=typer.colors.RED, err=True)
                    if sys.version_info.minor < 10:
                        typer.secho(
                            'This is probably a bug in Python itself. '
                            'See https://github.com/FNNDSC/caw/issues/12',
                            fg=typer.colors.YELLOW, err=True
                        )
                    pool.shutdown(cancel_futures=True)  # fail fast
                    raise typer.Abort()
                progress.update(1)
                return target.stat().st_size

            sizes = pool.map(download_file, to_download)

    total_size = sum(sizes)
    if total_size < 2e5:
        size = f'{total_size} bytes'
    elif total_size < 2e8:
        size = f'{total_size / 1e6:.4f} MB'
    else:
        size = f'{total_size / 1e9:.4f} GB'
    typer.secho(size, fg=typer.colors.GREEN, err=True)


def _discover_files_to_download(client: ChrisClient, url: CUBEUrl) -> Tuple[DownloadableFile, ...]:
    typer.echo('Discovering files... ', nl=False)
    total = 0

    def report_discovered_file(f: DownloadableFile) -> DownloadableFile:
        nonlocal total
        total += 1
        typer.echo(f'\rDiscovering files... {total}', nl=False)
        return f

    try:
        search = tuple(report_discovered_file(f) for f in client.get_files(url))
    except TooMuchPaginationException:
        typer.echo(
            f'Number of paginated requests exceeded {MAX_REQUESTS}.'
            f"If you're trying to download many files, you can increase the limit:"
            f'\n\n\t {" ".join([ "env", f"{REQUESTS_ENV_VAR_NAME}={MAX_REQUESTS + 99900}"] + sys.argv)}\n'
        )
        raise typer.Abort()
    typer.echo(f'\rFound {total} files to download.')
    return search
