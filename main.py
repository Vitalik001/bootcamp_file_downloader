import asyncio
import requests

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



async def download_url():
    global current_downloads
    # url = input("Please enter the file url to download:")
    url = "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"
    response = requests.get(url)
    source, name = url.split("/")[-2:]
    if response.status_code == 200:

        print(f"Started downloading a file from {source}")
        current_downloads+=1
        print(f"Downloading {current_downloads} files")

        with open(name, "wb") as file:
            file.write(response.content)

        print("File downloaded successfully.")
        current_downloads-=1
    else:
        print(f"Failed to download file from {source}. Status code: {response.status_code}")




async def main():
    await download_url()
    print("All files finished downloading")

if __name__=="__main__":
    asyncio.run(main())

