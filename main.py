import asyncio
import aiohttp
import time

current_downloads = 0
urls = ["https://images.pexels.com/photos/358457/pexels-photo-358457.jpeg", \
            "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg",\
            "https://res.cloudinary.com/demo/image/upload/bo_1px_solid_gray/f_auto,q_auto/docs/jackie-favicon.png",\
            "https://res.cloudinary.com/demo/images/ar_1.0,c_thumb,g_face,w_0.6,z_0.7/r_max/co_brown,e_outline/t8sn7wg4jd74j/baloncesto-juego.jpg",\
            "https://res.cloudinary.com/demo/image/upload/a_45/c_scale,w_200/d_avatar.png/non_existing_id.png"]

async def handle_url(session, url):

    global current_downloads
    source, name = url.split("/")[-2:]

    response = await session.get(url, ssl=False)

    print(f"Started downloading a file from {source}")
    current_downloads += 1
    print(f"Downloading {current_downloads} files")

    if response.status == 200:
        with open(name, "wb") as file:
            async for chunk in response.content.iter_any():
                file.write(chunk)

        print("File downloaded successfully.")
        current_downloads -= 1

        if current_downloads == 0:
            print("All files finished downloading")

    else:
        print(f"Failed to download file from {source}. Status code: {response.status}")


async def main():

    print("Please enter the file url to download:")

    async with aiohttp.ClientSession() as session:

        tasks = []

        while (url := input()) != "exit":
        # for url in urls:
            print(url)
            tasks.append(asyncio.create_task(handle_url(session, url)))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end-start)
