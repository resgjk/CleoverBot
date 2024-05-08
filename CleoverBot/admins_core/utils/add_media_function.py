from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile


def add_media(text, photos, videos):
    media = []
    if photos:
        for photo in photos:
            if not media:
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
            if not media:
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
