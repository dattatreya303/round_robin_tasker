from telegram.ext import MessageHandler, Filters

from conversations.callbacks.root_handler_callbacks import root_router_v2

ROUTER_HANDLER = MessageHandler(Filters.text | Filters.command, callback=root_router_v2)
