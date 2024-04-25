import asyncio
import telegram
import re
import traceback
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyParameters,
    InputMediaPhoto,
    InputMediaVideo,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

import config
import util
from util.log import logger
from plugin import handler, load_plugins

import nest_asyncio
nest_asyncio.apply()

def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None) -> None:
    message = update.message
    if not message:
        message = update.edited_message
    logger.info(message)
    logger.info(message.text_html)
    if text is None:
      text = (
        message.text
        .replace("@"+config.bot.username, "")
        .replace("/start", "")
        .strip()
      )
    if text[0] == "/":
      return
    
    if message.chat.id != config.echo_chat_id != 0:
      name = message.chat.first_name + " " + (message.chat.last_name if message.chat.last_name else '')
      keyboard = [
        [
            InlineKeyboardButton(name, url=f"tg://user?id={message.chat.id}"),
        ],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      
      await context.bot.copyMessage(
        chat_id=config.echo_chat_id, 
        message_id=message.message_id, 
        from_chat_id=message.chat.id,
        reply_markup=reply_markup,
      )
    elif config.echo_chat_id != 0:
      if message.reply_to_message.reply_markup and message.reply_to_message.reply_markup.inline_keyboard:
        reply_to_message_id = None
        if len(message.reply_to_message.parse_entities()) > 0:
          logger.info(enumerate(message.reply_to_message.parse_entities()))
        await context.bot.sendMessage(
          chat_id=message.reply_to_message.reply_markup.inline_keyboard[0][0].url.replace('tg://user?id=', ''), 
          text=message.text_html, 
          parse_mode="HTML",
          reply_to_message_id=reply_to_message_id
        )
      
    for i in config.commands:
      if i.private_pattern is not None and str(message.chat.type) == "private" and re.search(i.private_pattern, text):
          return await i.func(update, context, text)
      if i.pattern is not None and re.search(i.pattern, text):
          return await i.func(update, context, text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot

    if update.message and update.message.chat.type != "private":
        return
      
    message = update.message
    logger.info(message)
    
    if message.chat.id != config.echo_chat_id != 0:
      name = message.chat.first_name + " " + (message.chat.last_name if message.chat.last_name else '')
      keyboard = [
        [
            InlineKeyboardButton(name, url=f"tg://user?id={message.chat.id}"),
        ],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
    
      await bot.copyMessage(
        chat_id=config.echo_chat_id, 
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=reply_markup,
      )
    elif config.echo_chat_id != 0:
      if message.reply_to_message.reply_markup and message.reply_to_message.reply_markup.inline_keyboard:
        await bot.copyMessage(
          chat_id=message.reply_to_message.reply_markup.inline_keyboard[0][0].url.replace('tg://user?id=', ''), 
          from_chat_id=message.chat.id,
          message_id=message.message_id,
        )
      
  
@handler('start')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, text):
    if len(text) <= 0:
        return await help(update, context)
    text = text.replace("_", " ").strip()
    logger.info(f"start: {text}")
    await handle(update, context, text)


@handler('help', info='介绍与帮助')
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, text=''):
    message = update.message
    name = message.chat.first_name 
    if message.chat.last_name:
      name += " " + message.chat.last_name
    return await update.message.reply_text(
        f'Hi, <a href="tg://user?id={message.chat.id}">{name}</a>! 这里是传话姬小派魔! \n'
        "发送任意内容，小派魔都会原话传达给主人~",
        parse_mode="HTML",
    )
    
    
@handler('roll', info='生成随机数 /roll [min=0] [max=9]')
async def roll(update, context, text):
    text = re.sub(r'(\d+)-(\d+)', r'\1 \2', text)
    arr = list(filter(lambda x: x != '', re.split(r' |/|~', text)))
    try:
      _min = int(arr[0])
    except Exception:
      _min = 0
    try:
      _max = int(arr[1])
    except Exception:
      _max = 9
    import random
    res = random.randint(_min, _max)
    return await update.message.reply_text(
      f'🎲 {res} in {_min} ~ {_max}' 
    )
    
    
async def main(app):
    bot: telegram.Bot = app.bot
    config.bot = await bot.get_me()
    
    app.add_error_handler(error_handler)
  
    load_plugins('plugins')
    for i in config.commands:
      app.add_handler(CommandHandler(i.cmd, i.func))
    
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO | filters.Document.ALL | filters.AUDIO | filters.Sticker.ALL, echo))
    app.add_handler(MessageHandler(filters.TEXT, handle))
    # app.add_handler(MessageHandler(filters.ALL, echo))
  
    commands = []
    for i in config.commands:
      if i.info != "":
        commands.append(BotCommand(i.cmd, i.info))
    await bot.set_my_commands(commands)
    
    
if __name__ == "__main__":
  app = (
      ApplicationBuilder()
      .token(config.token)
      .proxy(config.proxy_url)
      .get_updates_proxy(config.proxy_url)
      .build()
  )
  asyncio.run(main(app))
  app.run_polling()  # 启动Bot