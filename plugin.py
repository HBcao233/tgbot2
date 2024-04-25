import traceback
import re
import os.path
import config
from util.log import logger


class Command:
  def __init__(self, cmd, func, pattern=None, private_pattern=None, info=""):
    self.cmd = cmd
    self.func = self(func)
    self.pattern = pattern
    self.private_pattern = private_pattern
    self.info = info
  
  def __str__(self):
    res = f'Command(cmd={self.cmd}, func={self.func}'
    if self.pattern is not None:
      res += f', pattern={self.pattern}'
    return res + ')'
    
  def __call__(self, func):
    def wrapper(update, context, text=None, *w_args, **w_kwargs):
        logger.info(update.message)
        if text is None:
          text = (
              update.message['text']
              .replace("@"+config.bot.username, "")
              .replace("/" + self.cmd, "")
              .replace(self.cmd, "")
              .replace("/start", "")
              .strip()
          )
        logger.info(text)
        return func(update, context, text, *w_args, **w_kwargs)
    return wrapper


class Inline:
  def __init__(self, func, pattern):
    self.func = func
    self.pattern = pattern
    
  def __str__(self):
    return f'Inline_Handler(func={self.func})'

class Button:
  def __init__(self, func, pattern):
    self.func = func
    self.pattern = pattern
    
  def __str__(self):
    return f'Button_Handler(func={self.func})'


def handler(cmd, **kwargs):
    def deco(func):
      config.commands.append(Command(cmd, func, **kwargs))
      return func
    return deco
    
    
def inline_handler(pattern):
  def deco(func):
    config.inlines.append(Inline(func, pattern))
    return func
  return deco
    
    
def button_handler(pattern):
  def deco(func):
    config.buttons.append(Button(func, pattern))
    return func
  return deco
  
  
def load_plugin(name):
  try:
    __import__(name, fromlist=[None])
    logger.info('Success to load plugin "' + name + '"')
  except Exception:
    logger.warning('Error to load plugin "' + name + '"')
    logger.warning(traceback.print_exc())
  
  
def load_plugins(dir_name):
  if not os.path.isdir(dir_name):
    os.mkdir(dir_name)
    
  for name in os.listdir(dir_name):
      path = os.path.join(dir_name, name)
      if os.path.isfile(path) and \
              (name.startswith('_') or not name.endswith('.py')):
          continue
      if os.path.isdir(path) and \
              (name.startswith('_') or not os.path.exists(
                  os.path.join(path, '__init__.py'))):
          continue
      m = re.match(r'([_A-Z0-9a-z]+)(.py)?', name)
      if not m:
          continue
      load_plugin(f'{dir_name}.{m.group(1)}')
        