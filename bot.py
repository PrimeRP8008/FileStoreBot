import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from motor.motor_asyncio import AsyncIOMotorClient

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID"))
DATABASE_URL = os.getenv("DATABASE_URL")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL")

# Initialize Bot
bot = Client("FileStoreBot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Connect to MongoDB
db_client = AsyncIOMotorClient(DATABASE_URL)
db = db_client['file_store_db']
users_col = db['users']
files_col = db['files']

# Start Command
@bot.on_message(filters.command("start"))
async def start(bot, message: Message):
    user_id = message.from_user.id
    await users_col.update_one({"_id": user_id}, {"$set": {"username": message.from_user.username}}, upsert=True)
    
    buttons = [[InlineKeyboardButton("Support Group", url="https://t.me/Woshang_Gang")]]
    
    await message.reply_text(
        f"Hello {message.from_user.first_name}!\nI am a File Store Bot.\nSend me a file, and I'll give you a shareable link.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Generate Link Command
@bot.on_message(filters.command("genlink"))
async def generate_link(bot, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("Reply to a document to generate a link.")
    
    file = message.reply_to_message.document
    file_id = file.file_id
    file_name = file.file_name
    file_size = file.file_size
    
    await files_col.insert_one({"file_id": file_id, "file_name": file_name, "file_size": file_size})
    
    await message.reply_text(f"Here is your file link:\nhttps://t.me/{bot.me.username}?start={file_id}")

# Batch Upload Mode
batch_mode = {}
@bot.on_message(filters.command("batch"))
async def batch_mode_toggle(bot, message: Message):
    user_id = message.from_user.id
    batch_mode[user_id] = not batch_mode.get(user_id, False)
    status = "enabled" if batch_mode[user_id] else "disabled"
    await message.reply_text(f"Batch mode {status}.")

# User Statistics Command
@bot.on_message(filters.command("stats"))
async def stats(bot, message: Message):
    user_count = await users_col.count_documents({})
    file_count = await files_col.count_documents({})
    await message.reply_text(f"Total Users: {user_count}\nTotal Files: {file_count}")

# Restart Command (Admin Only)
@bot.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart(bot, message: Message):
    await message.reply_text("Restarting bot...")
    os.system("kill -9 $(pgrep -f bot.py) && python3 bot.py")

# Force Subscribe System
@bot.on_message(filters.command("fsub"))
async def force_sub(bot, message: Message):
    await message.reply_text(f"Users must join: https://t.me/{TeamAnimePedia}")

# Run Bot
bot.run()
