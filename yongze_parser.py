from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import json
import logging
import sys
import time

def get_bot_key():
    api_key = ''
    with open("botapi.txt", "r") as f:
        api_key = f.read() 
    
    return api_key

def get_yz_dict():
    with open("yz_dict.json", "r") as yz_dict:
        data = json.load(yz_dict)

    return data

YZ_DICT = get_yz_dict()
WORD, DEFINITION, SAVE = range(3)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="sigh... what did yz smoke now?"
    )


def decrypt(update, context):
    cancer_list = update.message.text.split(" ")
    cancer_is_gone = list()

    for word in cancer_list:
        word = word.lower()
        if word in YZ_DICT.keys():
            cancer_is_gone.append(YZ_DICT[word])
        else:
            cancer_is_gone.append(word)
    
    resp = ' '.join(cancer_is_gone)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=resp
    )


def add_smoke_word(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="omg a new word? what is the word?"
    )
  

def add_smoke_definition(update, context):
    context.user_data["word"] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="wtf does that mean?"
    )

def save_new_smokes(update, context):
    word = context.user_data["word"]
    definition = update.message.text

    resp = "so YZ means {} when he says {}? Adding that to the cancer dictionary".format(definition, word)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=resp
    )

    if word in YZ_DICT.keys():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="that word is already in the dictionary tho..."
        )

        return ConversationHandler.END
    else:
        YZ_DICT[word] = definition

        with open("yz_dict.json", "w") as fp:
            json.dump(YZ_DICT, fp)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="added to dictionary!"
        )

        return ConversationHandler.END
    

def main():
    try:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        api_key = get_bot_key() 
    
        updater = Updater(token=api_key, use_context=True)
        dispatcher = updater.dispatcher

        convo_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
                MessageHandler(Filters.text & (~Filters.command), decrypt )
                ],

            states = {
                WORD: [CommandHandler('add', add_smoke_word)],
                DEFINITION: [MessageHandler(Filters.text & (~Filters.command), add_smoke_definition)],
                SAVE: [MessageHandler(Filters.text & (~Filters.command), save_new_smokes)]
            },

            fallbacks=[]
        )

        dispatcher.add_handler(convo_handler)
    except Exception as e:
        logging.exception(e)
        sys.exit()
    # start_handler = CommandHandler('start', start)
    # dispatcher.add_handler(start_handler)

    # message_handler = MessageHandler(Filters.text & (~Filters.command), decrypt)
    # dispatcher.add_handler(message_handler)

    while True:
        try:
            updater.start_polling(0.1)
        except KeyboardInterrupt:
            updater.stop()
        except Exception as e:
            logging.exception(e)
            time.sleep(15)

if __name__ == "__main__":
    main()
