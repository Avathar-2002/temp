import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import nest_asyncio

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Channel mappings for different categories
CHANNELS = {
    "PREDVD": [-1002155271116,-1002142404532],
    "HD": [-1002034649098],
    "WEBSERIES": [-1002134895451],  # Example channel for WebSeries
    "CWC": [-1002597802363],        # Example channel for CWC
    "ANIME": [-1001925884031],      # Example channel for Anime
    "HOLLYWOOD": [-1002053359396]   # Example channel for Hollywood
}

# Fixed channels for additional notification
FIXED_CHANNELS = [ -1002080923975,-1002069859850,-1001931456422,-1002083893325,-1004288598194,"@A1Moviepublic1","@A1Movies_p3"] 

# Store the movie data for each user
user_movie_data = {}

# Set up logging to display errors and debug messages
logging.basicConfig(level=logging.DEBUG)

def process_caption(caption: str) -> str:
    """
    Process the caption to extract meaningful content for the movie title.
    """
    lines = caption.split("\n")
    result = []

    for line in lines:
        if line.strip():
            result.append(line.strip())
        else:
            break

    return "\n".join(result)

def generate_movie_post(title, link, permanent_link, category=None):
    base_post = f"""
*{title}* 

✔️ *Sample* : 

♟*How To Download* ➡️

*Link* - [Click Here](https://www.instagram.com/reel/C3mQK9-PCLd/?igsh=MWdhaXVhN3E3NWFldA==)

🛡 *Download*:

*1080p*➡️
*Link* - *{link}*

*720p*➡️
*Link* - *{link}*

*480p*➡️
*Link* - *{link}*

*360p*➡️
*Link* - *{link}*

🛸 *Use Below Link for Permanent storage and also the above link not function* 

*Link* - *{permanent_link}*

⭘ *Join Our Channel For Direct Link* ⬇️⬇️⬇️
*https://t.me/+stEaOKChsEs3MTBl*
"""
    return base_post.strip()

def generate_additional_message(title, category=None):
    if category == "HD":
        return f"""
🎬 *{title}* 

*Download Full Movie From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+D8e3LO3tI5QzMTE1
🔹https://t.me/+D8e3LO3tI5QzMTE1
🔹https://t.me/+D8e3LO3tI5QzMTE1
"""
    elif category == "PREDVD":
        return f"""
🎬 *{title}* 

*Download Full Movie From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+n3ywsV6qaMMyMTY1
🔹https://t.me/+n3ywsV6qaMMyMTY1
🔹https://t.me/+n3ywsV6qaMMyMTY1
"""
    elif category == "WEBSERIES":
        return f"""
🎬 *{title}* 

*Download Full WebSeries From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+r2cT-gZoPz9lZWQ1
🔹https://t.me/+r2cT-gZoPz9lZWQ1
🔹https://t.me/+r2cT-gZoPz9lZWQ1
"""
    elif category == "CWC":
        return f"""
🎬 *{title}* 

*Download Full CWC Content From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+AsE--zL6sxA3MmM1
🔹https://t.me/+AsE--zL6sxA3MmM1
🔹https://t.me/+AsE--zL6sxA3MmM1
"""
    elif category == "ANIME":
        return f"""
🎬 *{title}* 

*Download Full Anime From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+ixEGzNnKiRNmYjRl
🔹https://t.me/+ixEGzNnKiRNmYjRl
🔹https://t.me/+ixEGzNnKiRNmYjRl
"""
    elif category == "HOLLYWOOD":
        return f"""
🎬 *{title}* 

*Download Full Hollywood Movie From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+Yk_I2U86MLBkNGY1
🔹https://t.me/+Yk_I2U86MLBkNGY1
🔹https://t.me/+Yk_I2U86MLBkNGY1
"""
    else:
        return f"""
🎬 *{title}* 

*Download Full Content From Below Channel* ⬇️⬇️⬇️

🔹https://t.me/+Oo9ifqO9MdxiNjU1
🔹https://t.me/+Oo9ifqO9MdxiNjU1
🔹https://t.me/+Oo9ifqO9MdxiNjU1
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("*Get Started*", callback_data="get_started")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "*Welcome to the Movie Bot! Please click the button below to get started.*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def get_started(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "*To use the bot, please follow the steps below:*\n\n"
        "• *Title*: Movie Title Extraction File\n"
        "• *Link*: <single link for all resolutions>\n"
        "• *Permanent*: <permanent link>\n\n"
        "*Once you've sent the text, upload the movie poster image manually.*",
        parse_mode="Markdown"
    )

async def handle_movie_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in user_movie_data:
        user_movie_data[update.message.from_user.id] = {}

    try:
        caption = update.message.caption
        if caption:
            title = process_caption(caption)
        else:
            title = None

        if not title:
            await update.message.reply_text("*Sorry, I couldn't find the title in the caption. Please make sure it's included in the caption text.*", parse_mode="Markdown")
            return

        user_movie_data[update.message.from_user.id]["title"] = title

        await update.message.reply_text(f"*I have extracted the title:* \n\n*{title}*\n\n"
                                      "*Now, please send the download link and permanent link in the following format:*\n\n"
                                      "*Link*: <URL for download>\n"
                                      "*Permanent*: <Permanent URL>",
                                      parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"*Error*: {str(e)}\n*Please ensure you're using the correct format.*", parse_mode="Markdown")

async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in user_movie_data or "title" not in user_movie_data[update.message.from_user.id]:
        await update.message.reply_text("*Please provide the movie title first by sending the movie caption.*", parse_mode="Markdown")
        return

    try:
        message = update.message.text.strip()
        lines = message.split("\n")

        if len(lines) < 2:
            await update.message.reply_text("*Please ensure you send the correct format:*\n\n"
                                          "*Link*: <URL for download>\n"
                                          "*Permanent*: <Permanent URL>",
                                          parse_mode="Markdown")
            return

        link = lines[0].replace("Link: ", "").strip()
        permanent_link = lines[1].replace("Permanent: ", "").strip()

        user_movie_data[update.message.from_user.id]["link"] = link
        user_movie_data[update.message.from_user.id]["permanent_link"] = permanent_link

        await update.message.reply_text("*Links received! Now, please upload the movie poster image.*", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"*Error*: {str(e)}\n*Please ensure you're using the correct format.*", parse_mode="Markdown")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in user_movie_data or "link" not in user_movie_data[update.message.from_user.id]:
        await update.message.reply_text("*Please provide the movie details first (title, link, and permanent link).*", parse_mode="Markdown")
        return

    if update.message.photo:
        image = update.message.photo[-1].file_id
        user_movie_data[update.message.from_user.id]["image"] = image

        keyboard = [
            [InlineKeyboardButton("HD", callback_data="hd"), 
             InlineKeyboardButton("PreDVD", callback_data="predvd")],
            [InlineKeyboardButton("WebSeries", callback_data="webseries"),
             InlineKeyboardButton("CWC", callback_data="cwc")],
            [InlineKeyboardButton("Anime", callback_data="anime"),
             InlineKeyboardButton("Hollywood", callback_data="hollywood")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("*Image received! Please specify the category.*", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    category = query.data.upper()
    logging.debug(f"Callback data received: {category}")

    if user_id not in user_movie_data or "image" not in user_movie_data[user_id]:
        await query.edit_message_text("*Please complete the previous steps first.*", parse_mode="Markdown")
        return

    movie_data = user_movie_data[user_id]
    base_caption = generate_movie_post(movie_data["title"], movie_data["link"], movie_data["permanent_link"], category)
    image = movie_data["image"]
    title = movie_data["title"]

    # Send to the bot itself first
    try:
        await context.bot.send_photo(
            chat_id=user_id, 
            photo=image, 
            caption=f"*Here's the post that was sent to channels:*\n\n{base_caption}",
            parse_mode="Markdown"
        )
        logging.info("Post successfully forwarded to the bot itself")
    except Exception as e:
        logging.error(f"Failed to forward to bot itself: {str(e)}")

    # Send to category-specific channels if they exist
    if category in CHANNELS:
        for channel in CHANNELS[category]:
            try:
                await context.bot.send_photo(
                    chat_id=channel, 
                    photo=image, 
                    caption=base_caption, 
                    parse_mode="Markdown"
                )
                logging.info(f"Base caption successfully forwarded to {category} channel: {channel}")
            except Exception as e:
                logging.error(f"Failed to forward to {category} channel {channel}: {str(e)}")

    # Send the additional message to fixed channels
    additional_message = generate_additional_message(title, category)
    for fixed_channel in FIXED_CHANNELS:
        try:
            await context.bot.send_photo(
                chat_id=fixed_channel, 
                photo=image, 
                caption=additional_message, 
                parse_mode="Markdown"
            )
            logging.info(f"Additional {category} message forwarded to fixed channel: {fixed_channel}")
        except Exception as e:
            logging.error(f"Failed to forward additional {category} message to fixed channel {fixed_channel}: {str(e)}")

    await query.edit_message_text("*Post successfully forwarded to the relevant channels!*", parse_mode="Markdown")
    del user_movie_data[user_id]

async def main():
    application = Application.builder().token("7376591969:AAEMIUTiB2Tusp2B8pVroM17B7QJUeLUDLQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(get_started, pattern="get_started"))
    application.add_handler(MessageHandler(filters.CAPTION, handle_movie_details))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(CallbackQueryHandler(handle_type_selection, pattern="^(hd|predvd|webseries|cwc|anime|hollywood)$"))

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
