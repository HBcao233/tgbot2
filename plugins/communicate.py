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
      [InlineKeyboardButton(name, url=f"tg://user?id={message.chat.id}")],
      [InlineKeyboardButton('data', callback_data=message.message_id)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    reply_to_message_id = None
    if (
      hasattr(message, 'reply_to_message') and 
      hasattr(message.reply_to_message, 'reply_markup') and
      (inline_keyboard := getattr(message.reply_to_message.reply_markup, 'inline_keyboard', None))
    ):
      reply_to_message_id = inline_keyboard[0][0].callback_data
      
    await bot.copyMessage(
      chat_id=config.echo_chat_id, 
      message_id=message.message_id, 
      from_chat_id=message.chat.id,
      reply_markup=reply_markup,
      reply_to_message_id=reply_to_message_id,
    )
    return
  
  if ( 
    hasattr(message, 'reply_to_message') and 
    hasattr(message.reply_to_message, 'reply_markup') and
    (inline_keyboard := getattr(message.reply_to_message.reply_markup, 'inline_keyboard', None))
  ):
    keyboard = [[InlineKeyboardButton('data', callback_data=message.message_id)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.copy_message(
      chat_id=inline_keyboard[0][0].url.replace('tg://user?id=', ''), 
      message_id=message.message_id,
      from_chat_id=message.chat.id,
      reply_markup=reply_markup,
      reply_to_message_id=inline_keyboard[1][0].callback_data,
    )
    