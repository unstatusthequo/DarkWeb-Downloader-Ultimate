# Darkweb Downloader Ultimate Edition

This Python script facilitates the anonymous downloading of files from URLs listed in a `urls.txt` file through the Tor network. The script ensures privacy by routing requests through Tor and provides real-time progress updates on the downloads, including download speed and percentage completion. This form handles multi-threaded downloads, zero byte file handling, and randomly timed retry queue to avoid givin up to quickly. Retries are set at 25, with a random number up to 300 seconds as a diff to avoid pattern blocking by the thread actors. 

## Features

- **Anonymity**: Uses Tor to anonymize your internet traffic.
- **Progress Tracking**: Real-time download speed with download time, size, and speed.
- **Logging**: Detailed logs of all successful and failed download activities.
- **User-Agent Customization**: Sends requests with a generic Mozilla user-agent to mimic typical user traffic.

## Prerequisites

Before running this script, make sure you have the following installed:
- Python 3.x
- Tor Browser or a standalone Tor service

## Dependencies

This script requires several Python libraries:
- `requests`
- `PySocks` (or `socks` depending on your environment)
- `tqdm`

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/alenperic/Darkweb-Downloader-Ultimate.git
   cd Darkweb-Downloader-Ultimate
   ```

2. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Tor**:
   Ensure that Tor is running and configured to accept connections through a SOCKS proxy (default is `localhost:9150` for Tor Browser).

4. **Set Up Configuration Files**:
   Edit the `urls.txt` file to include the URLs you wish to download files from.

## Usage
Add links to be downloaded to the urls.txt file.
Run the script using:

```bash
python download.py
```

The files will be downloaded to the `downloaded_files` directory, and progress will be shown in the command line interface. 

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request.
