import os

from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile


def add_media(text=None, photos=None, videos=None):
    media = []
    if photos:
        for photo in photos:
            if os.path.exists(photo):
                if not (media) and text:
                    media.append(
                        InputMediaPhoto(
                            type="photo", media=FSInputFile(path=photo), caption=text
                        )
                    )
                else:
                    media.append(
                        InputMediaPhoto(type="photo", media=FSInputFile(path=photo))
                    )
    if videos:
        for video in videos:
            if os.path.exists(video):
                if not (media) and text:
                    media.append(
                        InputMediaVideo(
                            type="video", media=FSInputFile(path=video), caption=text
                        )
                    )
                else:
                    media.append(
                        InputMediaVideo(type="video", media=FSInputFile(path=video))
                    )
    return media
