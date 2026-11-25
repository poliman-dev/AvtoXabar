import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylni tekshiring.")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# 1. Asosiy menyu tugmalari
button1 = KeyboardButton(text="🆕 Avto yangiliklar")
button2 = KeyboardButton(text="🚘 Avtomobillar haqida")
button3 = KeyboardButton(text="📊 Mashinalar reytingi")
button4 = KeyboardButton(text="🛠 Haydovchilar uchun maslahat")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button1, button2],
        [button3, button4]
    ],
    resize_keyboard=True
)

# 2. "Avtomobillar haqida" bo'limi uchun ichki (Inline) tugmalar
cars_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚙 Chevrolet", callback_data="car_chevrolet"),
            InlineKeyboardButton(text="⚡ BYD", callback_data="car_byd")
        ],
        [
            InlineKeyboardButton(text="🚘 Kia", callback_data="car_kia"),
            InlineKeyboardButton(text="🏎 Hyundai", callback_data="car_hyundai")
        ]
    ]
)

# 3. Start komandasi
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! Avto-Olam botiga xush kelibsiz! 🚘\n"
        "Avtomobillar haqida eng so'nggi yangiliklar va foydali ma'lumotlarni shu yerdan topasiz.\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=keyboard
    )

# 4. Help komandasi
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Botdan foydalanish uchun pastdagi tugmalardan birini bosing:\n\n"
        "🆕 Avto yangiliklar — O'zbekiston va jahon avto yangiliklari\n"
        "🚘 Avtomobillar haqida — Mashhur markalar texnik ma'lumotlari\n"
        "📊 Mashinalar reytingi — Eng ishonchli va tejamkor avtomobillar\n"
        "🛠 Haydovchilar uchun maslahat — Avtomobilni parvarish qilish sirlari",
        reply_markup=keyboard
    )

# 5. Avto yangiliklar tugmasi
@dp.message(F.text == "🆕 Avto yangiliklar")
async def auto_news(message: Message):
    await message.answer(
        "📰 <b>So'nggi avto yangiliklar:</b>\n\n"
        "1. O'zbekistonda elektromobillar uchun quvvatlash stansiyalari soni 2 barobarga oshirilmoqda.\n"
        "2. Yangi avlod gibrid avtomobillar yoqilg'i sarfini 100 kmga 3.8 litrgacha tushirdi.\n"
        "3. Yo'l harakati qoidalariga kiritilgan so'nggi o'zgarishlar bilan tanishing.",
        parse_mode="HTML"
    )

# 6. Avtomobillar haqida tugmasi (Ichki tugmalarni chiqaradi)
@dp.message(F.text == "🚘 Avtomobillar haqida")
async def about_cars(message: Message):
    await message.answer(
        "Qaysi avtomobil brendi haqida ma'lumot olmoqchisiz? Tanlang:",
        reply_markup=cars_inline_kb
    )

# 6.1. Ichki tugmalar bosilganda ishlaydigan qism (Callback)
@dp.callback_query(F.data.startswith("car_"))
async def car_details(callback: CallbackQuery):
    brand = callback.data.split("_")[1]
    
    info = {
        "chevrolet": (
            "🚙 <b>Chevrolet (O'zbekiston bozori yetakchisi)</b>\n\n"
            "• Mashhur modellari: Cobalt, Onix, Tracker, Malibu XL.\n"
            "• Afzalligi: Ehtiyot qismlar arzon va har joyda topiladi, ikkilamchi bozorda narxini yo'qotmaydi."
        ),
        "byd": (
            "⚡ <b>BYD (Elektromobil va Gibrid texnologiyalar)</b>\n\n"
            "• Mashhur modellari: Song Plus, Chazor, Han, Seagull.\n"
            "• Afzalligi: Blade Battery xavfsiz batareyasi, zamonaviy salon va juda kam xarajat."
        ),
        "kia": (
            "🚘 <b>Kia (Zamonaviy dizayn va qulaylik)</b>\n\n"
            "• Mashhur modellari: K5, Sportage, Sonet, Sorento.\n"
            "• Afzalligi: Yumshoq yurish qismi, boy komplektatsiya va 5 yillik rasmiy kafolat."
        ),
        "hyundai": (
            "🏎 <b>Hyundai (Ishonchlilik va texnologiya)</b>\n\n"
            "• Mashhur modellari: Elantra, Tucson, Sonata, Santa Fe.\n"
            "• Afzalligi: Chidamli dvigatellar, yuqori xavfsizlik tizimlari va qulay boshqaruv."
        )
    }
    
    await callback.message.edit_text(
        text=info[brand],
        reply_markup=cars_inline_kb,
        parse_mode="HTML"
    )
    await callback.answer()

# 7. Mashinalar reytingi tugmasi
@dp.message(F.text == "📊 Mashinalar reytingi")
async def car_ratings(message: Message):
    await message.answer(
        "🏆 <b>Eng yaxshi avtomobillar reytingi:</b>\n\n"
        "🥇 <b>Eng tejamkor:</b> BYD Chazor / Toyota Prius\n"
        "🥈 <b>Eng chidamli:</b> Toyota Camry / Chevrolet Cobalt\n"
        "🥉 <b>Eng qulay krossover:</b> Kia Sportage / Hyundai Tucson\n"
        "⚡ <b>Eng ommabop elektromobil:</b> BYD Song Plus EV",
        parse_mode="HTML"
    )

# 8. Haydovchilar uchun maslahat tugmasi
@dp.message(F.text == "🛠 Haydovchilar uchun maslahat")
async def driver_tips(message: Message):
    await message.answer(
        "🔧 <b>Haydovchilar uchun 4 ta oltin qoida:</b>\n\n"
        "1. <b>Dvigatel moyi:</b> Har 7 000 – 8 000 km da sifatli moy va filtrni almashtiring.\n"
        "2. <b>Shinalar bosimi:</b> Oyiga kamida 2 marta shinalar bosimini tekshiring — bu yoqilg'ini 5-10% tejaydi.\n"
        "3. <b>Qizdirish:</b> Sovuq havoda mashinani yurgizishdan oldin kamida 1-2 daqiqa qizdiring.\n"
        "4. <b>Akkumulyator:</b> Qish kelishidan oldin akkumulyator quvvatini tekshirtiring.",
        parse_mode="HTML"
    )

# 9. Noma'lum xabarlar
@dp.message()
async def unknown(message: Message):
    await message.answer(
        "Kechirasiz, bu xabarni tushunmadim. 🤔\n"
        "Pastdagi menyu tugmalaridan foydalaning."
    )

# 10. Botni ishga tushirish
async def main():
    print("Avto-Olam boti ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())