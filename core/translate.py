"""
Mijozga ko'rinadigan matnlarni rus va ingliz tillariga o'giruvchi qatlam.

Bot matnlari o'zbekcha yozilgan. Telegram'ga ketayotgan har bir so'rovdagi
(matn, izoh, tugma, alert) o'zbekcha iboralar foydalanuvchi tiliga qarab almashtiriladi.
Yangi matn qo'shilsa — shu yerdagi PHRASES lug'atiga (uz: (ru, en)) qo'shing.
O'zbek tilida hech narsa o'zgarmaydi.
"""
from contextvars import ContextVar
from typing import Dict, Optional

SUPPORTED = ("uz", "ru", "en")

# Joriy so'rov (update) tili — handler ichidagi chaqiruvlar uchun
current_lang: ContextVar[str] = ContextVar("current_lang", default="uz")

# telegram_id -> til (xotirada)
_LANG_CACHE: Dict[int, str] = {}


def remember_lang(telegram_id: Optional[int], lang: Optional[str]) -> None:
    if telegram_id and lang in SUPPORTED:
        _LANG_CACHE[int(telegram_id)] = lang


def cached_lang(telegram_id: int) -> Optional[str]:
    return _LANG_CACHE.get(int(telegram_id))


# uz: (ru, en)
PHRASES: Dict[str, tuple] = {
    # ── Asosiy menyu ───────────────────────────────────────
    "Bu PUBG Mobile va o'yin akkauntlari do'koni boti! Kerakli bo'limni tanlang va qulay xarid qiling.": (
        "Это магазин PUBG Mobile и игровых аккаунтов! Выберите нужный раздел и покупайте с удобством.",
        "This is the PUBG Mobile and game accounts store bot! Pick a section and shop with ease."),
    "PUBG Mobile va o'yin akkauntlari do'koni boti!": (
        "Бот-магазин PUBG Mobile и игровых аккаунтов!", "PUBG Mobile and game accounts store bot!"),
    "Salom,": ("Здравствуйте,", "Hello,"),
    "Asosiy menyu": ("Главное меню", "Main menu"),
    "Referal tizimi": ("Реферальная система", "Referral system"),
    "Qo'llab-quvvatlash": ("Поддержка", "Support"),
    "To'ldirish": ("Пополнить", "Top up"),
    "Foydali": ("Полезное", "Useful"),
    "Profilga qaytish": ("Назад в профиль", "Back to profile"),
    "Profil": ("Профиль", "Profile"),
    # ── Umumiy tugmalar ────────────────────────────────────
    "Orqaga": ("Назад", "Back"),
    "Bekor qilish": ("Отмена", "Cancel"),
    "Bekor qilindi.": ("Отменено.", "Cancelled."),
    "Tasdiqlash": ("Подтвердить", "Confirm"),
    "Rad etish": ("Отклонить", "Reject"),
    "Sotib olish": ("Купить", "Buy"),
    "Hozircha mavjud emas": ("Пока нет в наличии", "Out of stock"),
    # ── Do'kon ─────────────────────────────────────────────
    "Mahsulotni tanlang — to'lov to'g'ridan-to'g'ri\nbalansingizdan yechiladi va ma'lumotlar bir lahzada beriladi.": (
        "Выберите товар — оплата списывается напрямую\nс вашего баланса, данные выдаются мгновенно.",
        "Choose a product — payment is deducted directly\nfrom your balance and the details are delivered instantly."),
    "Hozircha mahsulotlar mavjud emas.\nTez orada qo'shiladi!": (
        "Пока товаров нет.\nСкоро появятся!", "No products yet.\nThey will be added soon!"),
    "Do'kon": ("Магазин", "Shop"),
    "Avtomatik yetkazib berish.": ("Автоматическая выдача.", "Automatic delivery."),
    "Xarid qilish uchun quyidagi tugmani bosing:": (
        "Нажмите кнопку ниже, чтобы купить:", "Press the button below to buy:"),
    "Narxi:": ("Цена:", "Price:"),
    "Mavjud:": ("В наличии:", "In stock:"),
    "Tavsif:": ("Описание:", "Description:"),
    "dona": ("шт.", "pcs"),
    "Xarid tasdiqlash": ("Подтверждение покупки", "Purchase confirmation"),
    "Sizning balansingiz:": ("Ваш баланс:", "Your balance:"),
    "Xaridni tasdiqlaysizmi?": ("Подтверждаете покупку?", "Confirm the purchase?"),
    "Xarid muvaffaqiyatli!": ("Покупка прошла успешно!", "Purchase successful!"),
    "Qolgan balans:": ("Остаток баланса:", "Remaining balance:"),
    "To'landi:": ("Оплачено:", "Paid:"),
    "Buyurtma:": ("Заказ:", "Order:"),
    "Mahsulot:": ("Товар:", "Product:"),
    "Sizning ma'lumotlaringiz:": ("Ваши данные:", "Your details:"),
    "Kategoriya topilmadi!": ("Категория не найдена!", "Category not found!"),
    "Mahsulot topilmadi!": ("Товар не найден!", "Product not found!"),
    "Mahsulot mavjud emas!": ("Товара нет в наличии!", "Product is unavailable!"),
    "Bu mahsulot endi sotilmaydi.": ("Этот товар больше не продаётся.", "This product is no longer sold."),
    "Afsuski, hozircha stokda yo'q!": ("К сожалению, сейчас нет в наличии!", "Sorry, currently out of stock!"),
    "Kechirasiz, hozircha stokda mahsulot yo'q. Admin bilan bog'laning!": (
        "Извините, товара пока нет в наличии. Свяжитесь с админом!",
        "Sorry, the product is out of stock. Please contact the admin!"),
    "Kechirasiz, mahsulot aynan hozir tugab qoldi! Iltimos, keyinroq urinib ko'ring.": (
        "Извините, товар только что закончился! Пожалуйста, попробуйте позже.",
        "Sorry, the product has just run out! Please try again later."),
    "Ma'lumot yetkazildi!": ("Данные выданы!", "Details delivered!"),
    "Balansingiz yetarli emas!": ("Недостаточно средств на балансе!", "Insufficient balance!"),
    "Yetishmaydi:": ("Не хватает:", "Missing:"),
    "Kerak:": ("Нужно:", "Required:"),
    "Balansni to'ldiring!": ("Пополните баланс!", "Please top up your balance!"),
    "Tizimda xatolik yuz berdi!": ("Произошла ошибка в системе!", "A system error occurred!"),
    "Ma'lumotni o'qishda xatolik. Admin bilan bog'laning.": (
        "Ошибка при чтении данных. Свяжитесь с админом.", "Error reading the data. Please contact the admin."),
    "Ma'lumotni o'qishda xatolik yuz berdi.": (
        "Произошла ошибка при чтении данных.", "An error occurred while reading the data."),
    "Ma'lumotni qanday olish kerak?": ("Как получить данные?", "How to receive the details?"),
    "@fakemailbot ga kiring va /start bosing.": (
        "Зайдите в @fakemailbot и нажмите /start.", "Open @fakemailbot and press /start."),
    "Yuqoridagi <b>pochta (login) va parolni</b> botga yuboring.": (
        "Отправьте боту <b>почту (логин) и пароль</b> выше.",
        "Send the <b>email (login) and password</b> above to the bot."),
    "Akkauntga kirishda kelgan <b>tasdiqlash kodini</b> shu bot orqali o'qib oling.": (
        "<b>Код подтверждения</b>, пришедший при входе в аккаунт, прочитайте через этого бота.",
        "Read the <b>verification code</b> sent during account login through this bot."),
    # ── Profil ─────────────────────────────────────────────
    "Sizning profilingiz": ("Ваш профиль", "Your profile"),
    "Ro'yxatdan o'tgan:": ("Дата регистрации:", "Registered:"),
    "Jami sarflangan:": ("Всего потрачено:", "Total spent:"),
    "Xaridlar:": ("Покупки:", "Purchases:"),
    "24 soat:": ("24 часа:", "24 hours:"),
    "7 kun:": ("7 дней:", "7 days:"),
    "Barcha vaqt:": ("За всё время:", "All time:"),
    "Balans:": ("Баланс:", "Balance:"),
    "Buyurtmalar tarixi": ("История заказов", "Order history"),
    "Chegirmalar va Promokodlar": ("Скидки и промокоды", "Discounts and promo codes"),
    "Chegirmalar": ("Скидки", "Discounts"),
    "Hozirda faol aksiyalar mavjud emas.\nYangi chegirmalar haqida bot kanalida e'lon qilinadi!": (
        "Сейчас нет активных акций.\nО новых скидках будет объявлено в канале бота!",
        "There are no active promotions right now.\nNew discounts will be announced in the bot channel!"),
    "Bot tili": ("Язык бота", "Bot language"),
    "Hozirgi til:": ("Текущий язык:", "Current language:"),
    "Siz hali hech qanday xarid amalga oshirmagansiz.": (
        "Вы ещё не совершали покупок.", "You haven't made any purchases yet."),
    "So'nggi 10 ta buyurtma. Tafsilot uchun raqamni bosing.": (
        "Последние 10 заказов. Нажмите на номер для подробностей.",
        "Last 10 orders. Tap a number for details."),
    "Buyurtma tafsiloti": ("Детали заказа", "Order details"),
    "Buyurtma topilmadi!": ("Заказ не найден!", "Order not found!"),
    "Noto'g'ri buyurtma!": ("Неверный заказ!", "Invalid order!"),
    "Buyurtma #": ("Заказ #", "Order #"),
    "Raqam:": ("Номер:", "Number:"),
    "Sana:": ("Дата:", "Date:"),
    "Holat:": ("Статус:", "Status:"),
    "Akkaunt ma'lumotlari topilmadi. Admin bilan bog'laning.": (
        "Данные аккаунта не найдены. Свяжитесь с админом.", "Account details not found. Please contact the admin."),
    "Akkaunt ma'lumotlari:": ("Данные аккаунта:", "Account details:"),
    "Avval ro'yxatdan o'ting: /start": ("Сначала зарегистрируйтесь: /start", "Please register first: /start"),
    # ── Balans ─────────────────────────────────────────────
    "Balansni to'ldirish": ("Пополнение баланса", "Top up balance"),
    "Hisobingizni to'ldirish uchun qulay to'lov usulini tanlang.\nMinimal to'lov:": (
        "Выберите удобный способ оплаты для пополнения счёта.\nМинимальный платёж:",
        "Choose a convenient payment method to top up your account.\nMinimum payment:"),
    "To'lov turini tanlang:": ("Выберите способ оплаты:", "Choose a payment method:"),
    "Karta orqali (Chek yuborish)": ("Картой (отправка чека)", "By card (send receipt)"),
    "Uzcard / Humo to'lov (Chek orqali)": ("Оплата Uzcard / Humo (по чеку)", "Uzcard / Humo payment (by receipt)"),
    "Hisobingizga qancha summa o'tkazmoqchi ekanligingizni so'mda yozib yuboring.\nMasalan:": (
        "Напишите в сумах, какую сумму хотите зачислить на счёт.\nНапример:",
        "Write the amount you want to add to your account, in UZS.\nFor example:"),
    "Minimal to'lov:": ("Минимальный платёж:", "Minimum payment:"),
    "yoki": ("или", "or"),
    "Noto'g'ri summa": ("Неверная сумма", "Invalid amount"),
    "Iltimos, faqat raqam kiriting.": ("Пожалуйста, вводите только цифры.", "Please enter numbers only."),
    "Summa juda kam": ("Сумма слишком мала", "Amount is too low"),
    "Minimal to'ldirish summasi:": ("Минимальная сумма пополнения:", "Minimum top-up amount:"),
    "Iltimos, qaytadan kiriting.": ("Пожалуйста, введите заново.", "Please enter again."),
    "To'lov uchun rekvizitlar": ("Реквизиты для оплаты", "Payment details"),
    "To'lov summasi:": ("Сумма платежа:", "Payment amount:"),
    "Karta raqami:": ("Номер карты:", "Card number:"),
    "Karta egasi:": ("Владелец карты:", "Cardholder:"),
    "To'lovdan keyin": ("После оплаты", "After payment"),
    "Ushbu botga to'lov <b>cheki (skrinshot)</b>ni yuboring. Tekshirilib, hisobingizga mablag' qo'shiladi.": (
        "Отправьте боту <b>чек об оплате (скриншот)</b>. После проверки средства поступят на ваш счёт.",
        "Send the <b>payment receipt (screenshot)</b> to this bot. After verification the funds will be added to your account."),
    "To'lov chekini yuboring": ("Отправьте чек об оплате", "Send the payment receipt"),
    "Iltimos, to'lov cheki <b>rasmini (skrinshot)</b> yoki faylini yuboring.": (
        "Пожалуйста, отправьте <b>фото (скриншот)</b> чека или файл.",
        "Please send a <b>photo (screenshot)</b> of the receipt or a file."),
    "Chekingiz qabul qilindi!": ("Ваш чек принят!", "Your receipt has been received!"),
    "So'rov:": ("Запрос:", "Request:"),
    "Miqdor:": ("Сумма:", "Amount:"),
    "Tekshirilmoqda": ("Проверяется", "Under review"),
    "Admin tekshirib, tez orada balansingizni to'ldiradi. Natija haqida shu yerda xabar olasiz.": (
        "Админ проверит и скоро пополнит ваш баланс. О результате вы узнаете здесь.",
        "The admin will review it and top up your balance soon. You will be notified here."),
    "Ulangan raqam:": ("Привязанный номер:", "Linked number:"),
    "Balansingiz to'ldirildi!": ("Ваш баланс пополнен!", "Your balance has been topped up!"),
    "Qo'shilgan miqdor:": ("Зачислено:", "Added:"),
    "Qo'shilgan:": ("Зачислено:", "Added:"),
    "Joriy balans:": ("Текущий баланс:", "Current balance:"),
    "Xaridlarni boshlashingiz mumkin": ("Можно начинать покупки", "You can start shopping"),
    "Balans so'rovingiz rad etildi": ("Ваш запрос на пополнение отклонён", "Your top-up request was rejected"),
    "Miqdor:": ("Сумма:", "Amount:"),
    "Chek tasdiqlanmadi yoki ma'lumotlar mos kelmadi.": (
        "Чек не подтверждён или данные не совпали.", "The receipt was not approved or the details did not match."),
    "Savol bo'lsa, qo'llab-quvvatlash bilan bog'laning.": (
        "Если есть вопросы, свяжитесь с поддержкой.", "If you have questions, contact support."),
    # ── Foydali ────────────────────────────────────────────
    "Foydali ma'lumotlar": ("Полезная информация", "Useful information"),
    "Botimiz 24/7 rejimda avtomatik ishlaydi.\nBarcha tovarlar xarid qilingan zahoti beriladi.\nKafolat va xavfsizlik 100% ta'minlangan!": (
        "Наш бот работает автоматически 24/7.\nВсе товары выдаются сразу после покупки.\nГарантия и безопасность 100%!",
        "Our bot works automatically 24/7.\nAll products are delivered immediately after purchase.\nGuarantee and security are 100% ensured!"),
    # ── Referal ────────────────────────────────────────────
    "Sizning taklif havolangiz:": ("Ваша пригласительная ссылка:", "Your invite link:"),
    "Statistikangiz:": ("Ваша статистика:", "Your statistics:"),
    "Jami takliflar:": ("Всего приглашений:", "Total invites:"),
    "Har bir do'stingiz xavfsizlik tekshiruvidan o'tgach hisobingizga bonus beriladi.": (
        "За каждого друга после проверки безопасности вам начисляется бонус.",
        "You get a bonus for each friend after the security check."),
    "Do'stlarga ulashish": ("Поделиться с друзьями", "Share with friends"),
    "Asosiy balansga o'tkazish": ("Перевести на основной баланс", "Transfer to main balance"),
    "asosiy balansingizga o'tkazildi!": ("переведено на ваш основной баланс!", "transferred to your main balance!"),
    "Minimal yechib olish summasi": ("Минимальная сумма вывода", "Minimum withdrawal amount"),
    "Sizda:": ("У вас:", "You have:"),
    "Foydalanuvchi topilmadi!": ("Пользователь не найден!", "User not found!"),
    "Xatolik! Balans yetarli emas.": ("Ошибка! Недостаточно средств.", "Error! Insufficient balance."),
    "Referal kodingiz mavjud emas. /start bosing.": (
        "У вас нет реферального кода. Нажмите /start.", "You don't have a referral code. Press /start."),
    "COIN DONAT BOT orqali o'yin akkauntlarini xarid qiling!": (
        "Покупайте игровые аккаунты через COIN DONAT BOT!", "Buy game accounts via COIN DONAT BOT!"),
    "Referal tizimi": ("Реферальная система", "Referral system"),
    "ta\n• Tasdiqlangan:": ("\n• Подтверждено:", "\n• Confirmed:"),
    "ta\n• Ishlangan summa:": ("\n• Заработано:", "\n• Earned:"),
    "Masalan:": ("Например:", "For example:"),
    "To'lov tekshirilmoqda": ("Платёж проверяется", "Payment under review"),
    "To'lov kutilmoqda": ("Ожидается оплата", "Awaiting payment"),
    "Yetkazishda xatolik": ("Ошибка выдачи", "Delivery error"),
    "Yetkazilmoqda": ("Выдаётся", "Being delivered"),
    "Bajarildi": ("Выполнен", "Completed"),
    "Bekor qilindi": ("Отменён", "Cancelled"),
    "Rad etildi": ("Отклонён", "Rejected"),
    # ── Birliklar (eng oxirida) ────────────────────────────
    "so'm": ("сум", "UZS"),
}

# Uzunroqlari birinchi almashtiriladi
_ORDERED = sorted(PHRASES.items(), key=lambda kv: len(kv[0]), reverse=True)
_IDX = {"ru": 0, "en": 1}


def translate_text(text: str, lang: str) -> str:
    if not text or lang not in _IDX:
        return text
    i = _IDX[lang]
    for src, tr in _ORDERED:
        if src in text:
            text = text.replace(src, tr[i])
    return text


def translate_markup(markup, lang: str):
    """Inline tugmalar matnini tarjima qiladi (o'zgarish bo'lsa yangi markup qaytaradi)."""
    rows = getattr(markup, "inline_keyboard", None)
    if not rows or lang not in _IDX:
        return markup
    changed = False
    new_rows = []
    for row in rows:
        new_row = []
        for btn in row:
            new_text = translate_text(btn.text, lang)
            if new_text != btn.text:
                changed = True
                btn = btn.model_copy(update={"text": new_text})
            new_row.append(btn)
        new_rows.append(new_row)
    return markup.model_copy(update={"inline_keyboard": new_rows}) if changed else markup
