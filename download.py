import requests
import os

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
                response = session.get(url)
                response.raise_for_status()  # Raises stored HTTPError, if one occurred

                # Save file
                file_name = url.split('/')[-1]
                file_path = os.path.join(download_folder, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")

# Example usage
download_files_from_darkweb('urls.txt', 'downloaded_files')
