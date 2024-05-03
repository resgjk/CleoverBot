from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile


def add_media(text, photos, videos):
    media = []
    if photos:
        for photo in photos:
            try:
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
            except Exception:
                pass
    if videos:
        for video in videos:
            try:
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
            except Exception:
                pass
    return media
