import asyncio
import aiohttp
from urllib.parse import urlparse

# https://drive.usercontent.google.com/download?id=1Hsr0Fspd9TSBI5dQ77mm_avyn-MWybUa&export=download&authuser=0&confirm=t&uuid=9859fa3e-6e15-4af6-9df6-248372bfdf2f&at=APZUnTU6RqTZpBLYf2KyDo9paddp:1691672020655
current_downloads = 0
lock = asyncio.Lock()
urls = ["https://drive.usercontent.google.com/download?id=1Hsr0Fspd9TSBI5dQ77mm_avyn-MWybUa&export=download&authuser=0&confirm=t&uuid=9859fa3e-6e15-4af6-9df6-248372bfdf2f&at=APZUnTU6RqTZpBLYf2KyDo9paddp:1691672020655", \
        "https://drive.usercontent.google.com/download?id=1DEHn8qewiIKvb22ChndM_e_Ln4LvP1g0&export=download&authuser=0&confirm=t&uuid=62a13df8-de5a-4f49-ac5c-a564061e9d80&at=APZUnTX2tAugmAwsmObdWW-xpli7:1691669429481", \
        "https://images.pexels.com/photos/358457/pexels-photo-358457.jpeg", \
        "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg",\
        "https://res.cloudinary.com/demo/image/upload/bo_1px_solid_gray/f_auto,q_auto/docs/jackie-favicon.png",\
        "https://res.cloudinary.com/demo/images/ar_1.0,c_thumb,g_face,w_0.6,z_0.7/r_max/co_brown,e_outline/t8sn7wg4jd74j/baloncesto-juego.jpg",\
        "https://res.cloudinary.com/demo/image/upload/a_45/c_scale,w_200/d_avatar.png/non_existing_id.png"]

async def handle_url(session, url):
    try:
        parsed_url = urlparse(url)
    except Exception:
        print("Invalid URL format")
        return

    source = parsed_url.netloc
    name = parsed_url.path.split("/")[-1]

    global current_downloads

    try:
        async with session.get(url, ssl=False) as response:
            response.raise_for_status()  # Raises an exception if the response status is not successful

            if response.status == 200:
                print(f"Started downloading file {name} from {source}")

                current_downloads += 1
                print(f"Downloading {current_downloads} files")

                with open(name, "wb") as file:
                    async for chunk in response.content.iter_any():
                        file.write(chunk)

                print(f"File {name} from {source} downloaded successfully.")

                current_downloads -= 1

                if current_downloads == 0:
                    print("All files finished downloading")
            else:
                print(f"Failed to download file {name} from {source}. Status code: {response.status}")
    except aiohttp.client_exceptions.InvalidURL:
        print(f"Invalid URL: {url}")
    except aiohttp.ClientResponseError as e:
        print(f"Error downloading {url}: {e.status}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")



async def main():

    print("Please enter the file url to download:")

    async with aiohttp.ClientSession() as session:

        tasks = []

        while True:
            url = await asyncio.get_running_loop().run_in_executor(None, input)
            # url = input()
            if url == "exit":
                break

            tasks.append(asyncio.create_task(handle_url(session, url)))


        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

