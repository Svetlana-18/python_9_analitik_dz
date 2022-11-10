from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Определяем константы этапов разговора
fld = list(range(1, 10))
x = chr(10060)
o = chr(11093)
count = 9
player = x
CHOICE = 0


def show_field(field):
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"-" * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'-' * 25}"
    return txt


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [field[x[0]] for x in win_coord if field[x[0]] == field[x[1]] == field[x[2]]]
    return n[0] if n else n


def start(update, _):
    global fld, player, count
    fld = list(range(1, 10))
    count = 9
    player = x
    update.message.reply_text("Привет, я телеграм-бот. Давай сыграем в крестики-нолики? Введи цифру поля хода")
    update.message.reply_text(show_field(fld))
    return CHOICE


def choice(update, _):
    global player, count
    move = update.message.text
    move = int(move)
    if move not in fld:
        update.message.reply_text(f"Неккоректный ввод{chr(9940)}\n")
    else:
        fld.insert(fld.index(move), player)
        fld.remove(move)
        update.message.reply_text(show_field(fld))
        if check_win(fld):
            update.message.reply_text(f"{player} - ПОБЕДА!{chr(127942)}{chr(127881)}")
            return ConversationHandler.END
        player = o if player == x else x
        count -= 1

    if count == 0:
        update.message.reply_text(f"НИЧЬЯ {chr(129309)}")
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('Выход', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater("5605526481:AAG9tx5MzA09nYUkPHA8Z_zkPtrpzmdg42M")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('server start')

    updater.start_polling()
    updater.idle()
