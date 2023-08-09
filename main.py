import asyncio
import requests
from threading import Lock

lock = Lock()
current_downloads = 0


# Implement asynchronous(using asyncio)
# command-line file downloader.
# The command line should read the file
# urls from the input, download the files
# and report the progress while not
# blocking the input, allowing adding new
# files to the downloads while other files
# are already being  downloaded.
# The files should be downloaded in parallel.
# Create a new github repo

# Please enter the file url to download:
# >http://example.com/file1.pdf
# Started downloading a file from example.com
# Downloading 1 files
# >http://example.com/file2.pdf
# Started downloading a file from example.com
# Downloading 2 files
# Finished downloading a file from example.com
# Downloading 1 files
# Finished downloading a file from example.com
# All files finished downloading


async def download_url(url):
    global current_downloads
    response = asyncio.create_task(requests.get(url))
    source, name = url.split("/")[-2:]
    await response
    if response.status_code == 200:

        print(f"Started downloading a file from {source}")
        with lock:
            current_downloads += 1
        print(f"Downloading {current_downloads} files")

        with open(name, "wb") as file:
            file.write(response.content)

        print("File downloaded successfully.")
        with lock:
            current_downloads -= 1
    else:
        print(f"Failed to download file from {source}. Status code: {response.status_code}")

    if current_downloads == 0:
        print("All files finished downloading")


async def main():
    print("Please enter the file url to download:")
    # url = "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"
    tasks = []
    while (url := input()) != "exit":
        tasks.append(asyncio.create_task(download_url(url)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
