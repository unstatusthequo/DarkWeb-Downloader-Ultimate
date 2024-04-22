import requests
import os
import logging
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='output.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def download_files_from_darkweb(file_path, download_folder):
    # Setup Tor connection
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:9150',
        'https': 'socks5h://localhost:9150'
    }
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'})

    # Ensure the download folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Read URLs from file
    with open(file_path, 'r') as file:
        urls = file.readlines()

    # Download each file
    for url in urls:
        url = url.strip()
        if url:
            try:
                # Start the download and setup the progress bar
                response = session.get(url, stream=True)
                response.raise_for_status()

                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kibibyte
                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True,
                                    desc=url.split('/')[-1], leave=False)

                file_name = url.split('/')[-1]
                file_path = os.path.join(download_folder, file_name)

                with open(file_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                progress_bar.close()

                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    print(f"ERROR, something went wrong downloading {url}")
                    logging.error(f"Download incomplete for {url}")
                else:
                    logging.info(f"Downloaded: {file_path}")
                    print(f"Downloaded: {file_path}")

            except Exception as e:
                error_message = f"Failed to download {url}: {e}"
                logging.error(error_message)
                print(error_message)
                if progress_bar:
                    progress_bar.close()

# Example usage
download_files_from_darkweb('urls.txt', 'downloaded_files')
