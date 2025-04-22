import os
import subprocess
import telebot
import time
import json
ascii_art = """
⠀

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


━━━━━━━━━━━━━━━━━━━━━━━━━━
[•] Made By  : Black Beard
[•] Telegram  : @Ilzci
[•] GITHUB    : BlackBeardDe
[•] VERSION   : 1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━

The script has been turned on the telegram bot
"""

print(ascii_art)
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('Your bot token')
LANG_FILE = "languages.json"


def load_languages():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_languages():
    with open(LANG_FILE, 'w') as f:
        json.dump(user_languages, f)

user_languages = load_languages()


messages = {
    'ar': {
        'processing': "تم استلام الملف، جاري المعالجة...",
        'invalid': "الملف يجب أن يكون بصيغة .webm فقط.",
        'success': "تم التحويل بنجاح!\nالوقت المستغرق: {duration} ثانية",
        'error': "حدث خطأ: {error}",
        'language_set': "تم تغيير اللغة إلى العربية.",
        'choose_lang': "اختر لغتك:",
    },
    'en': {
        'processing': "File received, processing...",
        'invalid': "The file must be in .webm format only.",
        'success': "Converted successfully!\nTime taken: {duration} seconds",
        'error': "An error occurred: {error}",
        'language_set': "Language changed to English.",
        'choose_lang': "Choose your language:",
    }
}

def get_lang(user_id):
    return user_languages.get(str(user_id), 'ar')

@bot.message_handler(commands=['start', 'lang'])
def send_language_buttons(message):
    lang = get_lang(message.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("العربية", callback_data='lang_ar'),
        InlineKeyboardButton("English", callback_data='lang_en')
    )
    bot.send_message(message.chat.id, messages[lang]['choose_lang'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_callback(call):
    lang_code = call.data.split('_')[1]
    user_id = str(call.from_user.id)
    user_languages[user_id] = lang_code
    save_languages()
    bot.edit_message_text(
        messages[lang_code]['language_set'],
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

@bot.message_handler(content_types=['video', 'document'])
def handle_file(message: Message):
    user_id = str(message.from_user.id)
    lang = get_lang(user_id)

    try:
        is_video = message.content_type == 'video'
        is_doc = message.content_type == 'document'

        file_id = message.video.file_id if is_video else message.document.file_id
        file_name = message.video.file_name if is_video else message.document.file_name

        bot.reply_to(message, messages[lang]['processing'])

        if not file_name.lower().endswith('.webm'):
            bot.send_message(message.chat.id, messages[lang]['invalid'])
            return

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        webm_filename = file_name
        mp4_filename = file_name.replace('.webm', '.mp4')

        with open(webm_filename, 'wb') as f:
            f.write(downloaded_file)

        start_time = time.time()

        cmd = f"ffmpeg -i \"{webm_filename}\" -c:v libx264 -preset fast -crf 28 \"{mp4_filename}\""
        subprocess.run(cmd, shell=True)

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        with open(mp4_filename, 'rb') as f:
            bot.send_video(message.chat.id, f, caption=messages[lang]['success'].format(duration=duration))

        os.remove(webm_filename)
        os.remove(mp4_filename)

    except Exception as e:
        bot.send_message(message.chat.id, messages[lang]['error'].format(error=str(e)))

bot.polling()