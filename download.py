import requests
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import logging
import warnings
import queue

# Setup logging and warnings
warnings.simplefilter('ignore', InsecureRequestWarning)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
success_logger = logging.getLogger("success")
failure_logger = logging.getLogger("failure")

handler_success = logging.FileHandler('success.log')
handler_failure = logging.FileHandler('failure.log')
handler_success.setLevel(logging.INFO)
handler_failure.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
handler_success.setFormatter(formatter)
handler_failure.setFormatter(formatter)

success_logger.addHandler(handler_success)
failure_logger.addHandler(handler_failure)

# Retry queue
retry_queue = queue.Queue()

def download_file(url, download_folder, session, is_retry=False):
    try:
        print(f"Downloading: {url}")
        response = session.get(url, stream=True, verify=False)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        file_name = url.split('/')[-1]
        file_path = os.path.join(download_folder, file_name)

        with open(file_path, 'wb') as file, tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=file_name) as progress_bar:
            for data in response.iter_content(1024):
                file.write(data)
                progress_bar.update(len(data))

        if os.path.getsize(file_path) == 0:
            raise ValueError("Downloaded file size is zero bytes, download likely failed.")

        success_logger.info(url)
        print(f"Successfully downloaded: {url}")
    except Exception as e:
        print(str(e))
        # Check if the file exists and is zero bytes before deciding to delete it
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)  # Delete the zero-byte file
            print(f"Deleted zero-byte file: {file_path}")
        if not is_retry:
            retry_queue.put((url, 1))  # Put failed download in retry queue with initial retry count
            print(f"Added to retry queue: {url}")
        else:
            failure_logger.info(url)
            print(f"Failed to download: {url}")

def handle_retries(download_folder, session, max_retries=25):
    while not retry_queue.empty():
        url, attempts = retry_queue.get()
        if attempts < max_retries:
            print(f"Retrying {url} (Attempt {attempts + 1}/{max_retries})")
            download_file(url, download_folder, session, is_retry=True)
            if attempts + 1 < max_retries:
                retry_queue.put((url, attempts + 1))  # Re-queue for another retry if needed
                print(f"Re-queued for another retry: {url}")
        else:
            print(f"Maximum retries reached for {url}")
            failure_logger.info(url)

def download_files_from_darkweb(file_path, download_folder, max_threads):
    session = requests.session()
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    with open(file_path, 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for url in urls:
            executor.submit(download_file, url, download_folder, session)

    handle_retries(download_folder, session)  # Handle retries after initial attempts

# Example usage
download_files_from_darkweb('urls.txt', 'downloaded_files', max_threads=10)
