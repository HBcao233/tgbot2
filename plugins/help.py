from telegram import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)
from plugin import handler


@handler('help', info='介绍与帮助')
async def help(update, context, text=''):
  message = update.message
  name = message.chat.first_name 
  if message.chat.last_name:
    name += " " + message.chat.last_name
  
  keyboard = [[
    InlineKeyboardButton("源代码", url=f"https://github.com/HBcao233/tgbot2"),
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)
  return await message.reply_text(
    f'Hi, <a href="tg://user?id={message.chat.id}">{name}</a>! 这里是传话姬小派魔! \n'
    "发送任意内容，小派魔都会原话传达给主人~",
    parse_mode="HTML",
    reply_markup=reply_markup,
  )
