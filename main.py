import asyncio
import aiohttp

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


# async def create_task(url):
#
#
#     await response
#     if response.status_code == 200:
#
#         print(f"Started downloading a file from {source}")
#
#         current_downloads += 1
#         print(f"Downloading {current_downloads} files")
#
#         with open(name, "wb") as file:
#             file.write(response.content)
#
#         print("File downloaded successfully.")
#         current_downloads -= 1
#     else:
#         print(f"Failed to download file from {source}. Status code: {response.status_code}")
#
#     if current_downloads == 0:
#         print("All files finished downloading")

async def handle_response(response, source, name):
    global current_downloads
    print(f"Started downloading a file from {source}")

    current_downloads += 1
    print(f"Downloading {current_downloads} files")

    with open(name, "wb") as file:
        async for chunk in response.content.iter_any():
            file.write(chunk)

    print("File downloaded successfully.")
    current_downloads -= 1


if current_downloads == 0:
    print("All files finished downloading")

async def main():
    print("Please enter the file url to download:")
    # url = "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"
    async with aiohttp.ClientSession() as session:

        while (url := input()) != "exit":
            source, name = url.split("/")[-2:]

            response = await session.get(url, ssl=False)

            if response.status == 200:

                await handle_response(response, source, name)

            else:
                print(f"Failed to download file from {source}. Status code: {response.status}")

    # await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
