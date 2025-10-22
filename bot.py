# bot.py
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN
from insta_scraper import scrape_instagram_user

# ----------------------
# Setup Bot & Dispatcher
# ----------------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----------------------
# Inline keyboard
# ----------------------
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🖼 Posts", callback_data="posts"),
        InlineKeyboardButton(text="🎬 Reels", callback_data="reels"),
        InlineKeyboardButton(text="🔖 Hashtags", callback_data="hashtags")
    ]
])

# ----------------------
# FSM States
# ----------------------
class Form(StatesGroup):
    waiting_for_username = State()
    waiting_for_hashtag = State()
    content_type = State()  # posts ou reels

# ----------------------
# /start handler
# ----------------------
async def start_handler(message: types.Message):
    await message.answer("Choisis une option :", reply_markup=menu_keyboard)

# ----------------------
# Button click handler
# ----------------------
async def callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    if query.data in ["posts", "reels"]:
        await state.set_state(Form.waiting_for_username)
        await state.update_data(content_type=query.data)
        await query.message.answer("Envoie le nom du compte Instagram :")
    elif query.data == "hashtags":
        await state.set_state(Form.waiting_for_hashtag)
        await query.message.answer("Envoie le hashtag (sans #) :")

# ----------------------
# Text handler (username / hashtag)
# ----------------------
async def text_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()

    # ---------- Username ----------
    if current_state == Form.waiting_for_username:
        username = message.text.strip()
        content_type = data.get("content_type", "posts")
        await message.answer(f"⏳ Recherche en cours pour **{username}**…")

        posts = await scrape_instagram_user(username, content_type=content_type)
        posts_sorted = sorted(posts, key=lambda x: int(x.get("likes", 0)), reverse=True)[:5]

        for i, post in enumerate(posts_sorted, start=1):
            text = f"🥇 TOP {i}\n\n📝 {post['caption']}\n❤️ Likes: {post.get('likes',0)}\n🔖 {' '.join(post['hashtags'])}\n🔗 {post['url']}"
            if content_type == "reels" and post.get("video"):
                await message.answer_video(video=post["video"], caption=text)
            elif post.get("image"):
                await message.answer_photo(photo=post["image"], caption=text)
            else:
                await message.answer(text)

        await state.clear()

    # ---------- Hashtag ----------
    elif current_state == Form.waiting_for_hashtag:
        hashtag = message.text.strip()
        await message.answer(f"⏳ Recherche des posts pour **#{hashtag}**…")

        posts = await scrape_instagram_user(hashtag)  # Utilise le scraping utilisateur pour hashtag
        all_hashtags = []
        for post in posts:
            all_hashtags.extend(post["hashtags"])

        hashtags_text = "\n".join(sorted(set(all_hashtags), key=all_hashtags.count, reverse=True)[:10])
        await message.answer(f"🔖 Top hashtags pour #{hashtag} :\n{hashtags_text}")
        await state.clear()

# ----------------------
# Register handlers
# ----------------------
dp.message.register(start_handler, F.text == "/start")
dp.message.register(text_handler)
dp.callback_query.register(callback_handler)

# ----------------------
# Run the bot
# ----------------------
if __name__ == "__main__":
    print("🤖 Bot prêt !")
    asyncio.run(dp.start_polling(bot))
