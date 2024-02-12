from config import *
import os
from pytube import YouTube
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile
import time
from aiogram.enums import ParseMode

bot = Bot(Token, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(f"<b>Assalomu alaykum, bu bot Youtube dan video yuklaydi\n"
                         "Linkni jonating 🤖</b>")


@dp.message()
async def text_message(message: types.Message):
    url = message.text
    yt = YouTube(url)
    if message.text.startswith == "https://youtu.be/" or "https://youtube.com/":
        del_mes = await message.answer("<b>Tekshirilmoqda 🔎</b>")
        await message.delete()

        time.sleep(5)
        dell = await message.answer("<b>Biroz kuting, yuklanmoqda-aa! 😊</b>")
        await bot.delete_message(message.chat.id, del_mes.message_id)

        await download_youtube_video(url, message, bot)
        await bot.delete_message(message.chat.id, dell.message_id)

    else:
        await message.answer("<b>Qandaydir xatolik yuz berdi qayta urining !")


async def download_youtube_video(url, message, bot):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4")
    stream.get_highest_resolution().download(f"video", f"{yt.title}")

    time.sleep(5)
    with open(f"video/{yt.title}", "rb") as video:
        result = await message.answer_video(
            BufferedInputFile(
                video.read(),
                filename=f"{yt.title}.mp4"
            ), caption=f"<b>{yt.title}</b>")
        os.remove(f"video/{yt.title}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
