from aiogram.client.session.middlewares.base import BaseRequestMiddleware

from core.emojis import _set_attr
from core.logger import logger
from core.translate import (
    cached_lang, current_lang, remember_lang, translate_markup, translate_text,
)


async def _lang_for_chat(chat_id) -> str:
    """Xabar oluvchining tili: avval xotira, so'ng baza; topilmasa — joriy update tili."""
    try:
        cid = int(chat_id)
    except (TypeError, ValueError):
        return current_lang.get()
    lang = cached_lang(cid)
    if lang:
        return lang
    try:
        from sqlalchemy import select
        from db.database import async_session
        from db.models.user import User
        async with async_session() as session:
            res = await session.execute(select(User.language).where(User.telegram_id == cid))
            lang = res.scalar_one_or_none()
        if lang:
            remember_lang(cid, lang)
            return lang
    except Exception as e:
        logger.debug(f"Til aniqlanmadi: {e}")
    return "uz"


class TranslateMiddleware(BaseRequestMiddleware):
    """
    Telegram'ga ketayotgan matn/izoh/tugma/alert matnlarini oluvchining tiliga
    (ru/en) o'giradi. O'zbek tilida hech narsa o'zgarmaydi. Xato bo'lsa —
    xabar o'zgartirilmasdan yuboriladi.
    """

    async def __call__(self, make_request, bot, method):
        try:
            chat_id = getattr(method, "chat_id", None)
            lang = await _lang_for_chat(chat_id) if chat_id is not None else current_lang.get()
            if lang != "uz":
                for attr in ("text", "caption"):
                    value = getattr(method, attr, None)
                    if isinstance(value, str) and value:
                        new_value = translate_text(value, lang)
                        if new_value != value:
                            _set_attr(method, attr, new_value)
                media = getattr(method, "media", None)
                caption = getattr(media, "caption", None)
                if isinstance(caption, str) and caption:
                    new_caption = translate_text(caption, lang)
                    if new_caption != caption:
                        _set_attr(method, "media", media.model_copy(update={"caption": new_caption}))
                markup = getattr(method, "reply_markup", None)
                if markup is not None and hasattr(markup, "inline_keyboard"):
                    new_markup = translate_markup(markup, lang)
                    if new_markup is not markup:
                        _set_attr(method, "reply_markup", new_markup)
        except Exception as e:
            logger.debug(f"Tarjima qo'llanmadi: {e}")
        return await make_request(bot, method)
