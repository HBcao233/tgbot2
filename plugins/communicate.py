from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import config 
from util import logger
from plugin import handler


@handler('_')
async def _(update, context, text):
  message = update.message 
  bot = context.bot
  # logger.info(message)
  if config.echo_chat_id == 0:
    return
  
  if message.chat.id != config.echo_chat_id:
    name = message.chat.first_name + " " + (message.chat.last_name if message.chat.last_name else '')
    keyboard = [
      [
          InlineKeyboardButton(name, url=f"tg://user?id={message.chat.id}"),
      ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await bot.copyMessage(
      chat_id=config.echo_chat_id, 
      message_id=message.message_id, 
      from_chat_id=message.chat.id,
      reply_markup=reply_markup,
    )
    return
  
  if ( 
    hasattr(message, 'reply_to_message') and 
    hasattr(message.reply_to_message, 'reply_markup') and
    getattr(message.reply_to_message.reply_markup, 'inline_keyboard', None)
  ):
    await bot.copy_message(
      chat_id=message.reply_to_message.reply_markup.inline_keyboard[0][0].url.replace('tg://user?id=', ''), 
      message_id=message.message_id,
      from_chat_id=message.chat.id,
    )
    