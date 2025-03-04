from pyrogram import filters
from FileStoreBox import app
from FileStoreBox.core import script
from FileStoreBox.core import main_func
from FileStoreBox.core import tools_func
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup




button = InlineKeyboardMarkup([
	[
          InlineKeyboardButton("Tool Box", callback_data="tools_")                
        ],
	[
          InlineKeyboardButton("Update Channel", url="https://t.me/TeamAnimePedia")                
        ]])



@app.on_message(filters.command("start") & filters.private)
async def start(_, message):        
    if message.text.startswith("/start FileBox"):
        await main_func.fetch_files(_, message)
        return 
        
    elif message.text.startswith("/start BatchBox"):
        await main_func.batch_files(_, message)
        return 
    else:
        await message.reply_photo(
            photo="https://envs.sh/Hpz.jpg",
            caption=script.START_TEXT.format(message.from_user.first_name),
            reply_markup=button
        )

  

buttons = InlineKeyboardMarkup([
      [
          InlineKeyboardButton("Database", callback_data="database_"),
          InlineKeyboardButton("Force", callback_data="force_"),
          InlineKeyboardButton("Shortener", callback_data="shortener_")
      ],[   
          InlineKeyboardButton("🔙 Back", callback_data="home_") 
      ]])



buttons1 = InlineKeyboardMarkup([
	  [                
                InlineKeyboardButton("✚ sᴇᴛ ᴅᴀᴛᴀʙᴀsᴇ", callback_data="set_database")
            ],[                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_database"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_database")
            ],[
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="tools_"),
            ]])


buttons2 = InlineKeyboardMarkup([
	  [                
                InlineKeyboardButton("✚ sᴇᴛ ғᴏʀᴄᴇ ᴄʜᴀɴɴᴇʟ", callback_data="set_force")
            ],[                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_force"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_force")
            ],[
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="tools_"),
            ]])


buttons3 = InlineKeyboardMarkup([
	  [                
                InlineKeyboardButton("✚ sᴇᴛ sʜᴏʀᴛᴇɴᴇʀ", callback_data="set_shortener")
            ],[                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_shortener"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_shortener")
            ],[
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="tools_"),
            ]])




@app.on_callback_query()
async def handle_callback(_, query):
    user_id = query.from_user.id
    if query.data == "home_":
        await query.message.edit_text(
            script.START_TEXT.format(query.from_user.mention),
            reply_markup=button
        )
    elif query.data == "tools_":
        await query.message.edit_text(
            script.TOOLS_TEXT,
            reply_markup=buttons
        )
    elif query.data == "database_":
        await query.message.edit_text(
            script.DATABASE_TEXT,
            reply_markup=buttons1
        )
    elif query.data == "force_":
        await query.message.edit_text(
            script.FORCE_TEXT,
            reply_markup=buttons2
        )
    elif query.data == "shortener_":
        await query.message.edit_text(
            script.SHORTENER_TEXT,
            reply_markup=buttons3
        )
	    
    elif query.data.startswith("set"):
        task = query.data.split("_")[1]
        if task == "database":
            await tools_func.add_channel(query)
        elif task == "force":
            await tools_func.add_force_channel(query)
        elif task == "shortener":
            await tools_func.add_shortener(query)
        else:
            print("unknown set query")

    elif query.data.startswith("rm"):
        task = query.data.split("_")[1]
        if task == "database":
            await tools_func.delete_channel(query)
        elif task == "force":
            await tools_func.delete_force_channel(query)
        elif task == "shortener":
            await tools_func.delete_shortener(query)
        else:
            print("unknown remove query")

    elif query.data.startswith("views"):
        task = query.data.split("_")[1]
        if task == "database":
            await tools_func.view_channel(query)
        elif task == "force":
            await tools_func.view_force_channel(query)
        elif task == "shortener":
            await tools_func.view_shortener(query)
        else:
            print("unknown view query")
		
    elif query.data.startswith("checksub"):
        await main_func.fetch_files(_, query.message, encrypt_mode=False, query=query)
	    
    elif query.data.startswith("batchSub"):
        await main_func.batch_files(_, query.message, encrypt_mode=False, query=query)
	
    elif query.data == "maintainer_":
        await query.answer(
            "sᴏᴏɴ.... \nʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ",
            show_alert=True
        )
    elif query.data == "close_data":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception as e:
            print(f"Error deleting messages: {e}")


		
