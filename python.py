import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

url = "https://wassitonline.anem.dz/postulation/prolongationDemande"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'مرحبًا! من فضلك، أرسل أولاً رقم التسجيل في الوكالة الوطنية للتشغيل (Numéro d’inscription ANEM).'
    )

def handle_anem(update: Update, context: CallbackContext) -> None:
    anem_number = update.message.text.strip()
    if not anem_number.isdigit():
        update.message.reply_text("يرجى إدخال رقم تسجيل صحيح.")
        return
    context.user_data['anem_number'] = anem_number
    update.message.reply_text('الآن، من فضلك، أرسل رقم التعريف الوطني (Numéro d\'identification nationale - NIN).')

def handle_nin(update: Update, context: CallbackContext) -> None:
    nin = update.message.text.strip()
    if not nin.isdigit():
        update.message.reply_text("يرجى إدخال رقم NIN صحيح.")
        return

    anem_number = context.user_data.get('anem_number')
    if not anem_number:
        update.message.reply_text("يرجى أولاً إرسال رقم التسجيل في الوكالة الوطنية للتشغيل (ANEM).")
        return

    data = {
        "num_inscription_anem": anem_number,
        "num_identification_nationale": nin,
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            update.message.reply_text("تم تقديم طلبك بنجاح! سنقوم بمعالجته في أقرب وقت.")
        else:
            update.message.reply_text(f"فشل تقديم الطلب. رمز الخطأ: {response.status_code}")
    except Exception as e:
        update.message.reply_text(f"حدث خطأ أثناء إرسال الطلب: {e}")

def main():
    TOKEN = "7814578110:AAEow4VR3yfYreNYzNsxhs48Jzy_uusJyU4"
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_anem))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_nin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
