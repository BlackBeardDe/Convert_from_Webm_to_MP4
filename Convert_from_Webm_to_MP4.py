import os
import subprocess
import telebot
import time
import json
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ملفات التخزين
TOKEN_FILE = "bot_token.txt"
CONFIG_FILE = "config.json"
LANG_FILE = "languages.json"

# ألوان للطباعة في التيرمكس (Console)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'  # أخضر
    WARNING = '\033[93m'  # أصفر
    FAIL = '\033[91m'     # أحمر
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_languages():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_languages():
    with open(LANG_FILE, 'w') as f:
        json.dump(user_languages, f)

def get_bot_token():
    config = load_config()

    # تحقق من خيار "لا تسألني مجدداً"
    if config.get("skip_token_prompt", False):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()

    # طلب التوكن أو تغييره
    print("\n[?] Do you want to change the Telegram Bot Token?")
    print("[1] Yes")
    print("[2] No")
    print("[3] No, and don't ask me again")
    choice = input(">>> ").strip()

    if choice == "1":
        token = input("[?] Enter your new Telegram bot token: ").strip()
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print(f"{Colors.OKGREEN}[+] The Token was successfully saved!{Colors.ENDC}")
        return token

    elif choice == "2":
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        else:
            print(f"{Colors.WARNING}[!] ملف التوكن غير موجود، الرجاء إدخال التوكن:{Colors.ENDC}")
            token = input(">>> ").strip()
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            print(f"{Colors.OKGREEN}[+] تم حفظ التوكن بنجاح!{Colors.ENDC}")
            return token

    elif choice == "3":
        config["skip_token_prompt"] = True
        save_config(config)
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        else:
            print(f"{Colors.WARNING}[!] ملف التوكن غير موجود، الرجاء إدخال التوكن:{Colors.ENDC}")
            token = input(">>> ").strip()
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            print(f"{Colors.OKGREEN}[+] تم حفظ التوكن بنجاح!{Colors.ENDC}")
            return token

    else:
        print(f"{Colors.WARNING}[!] خيار غير صحيح، سيتم استخدام التوكن السابق إذا وجد.{Colors.ENDC}")
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        else:
            token = input("[?] Enter your Telegram bot token: ").strip()
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            print(f"{Colors.OKGREEN}[+] تم حفظ التوكن بنجاح!{Colors.ENDC}")
            return token

# تحميل اللغات والبيانات
user_languages = load_languages()

messages = {
    'ar': {
        'processing': "تم استلام الملف، جاري المعالجة...",
        'invalid': "الملف يجب أن يكون بصيغة .webm فقط.",
        'success': "تم التحويل بنجاح!\nالوقت المستغرق: {duration} ثانية",
        'error': "حدث خطأ: {error}",
        'language_set': "تم تغيير اللغة إلى العربية.",
        'choose_lang': "اختر لغتك:",
        'settings': "⚙️ الإعدادات",
        'cancel': "إلغاء",
        'change_token': "تعديل التوكن",
        'settings_info': "⚙️ الإعدادات:\n\nتوكن البوت الحالي:\n`{token}`\n\nهل تريد تعديل التوكن؟",
        'ask_new_token': "أرسل التوكن الجديد الآن:",
        'token_updated': "تم تحديث التوكن بنجاح! ✅",
        'token_invalid': "التوكن غير صالح! حاول مرة أخرى.",
        'cancelled': "تم الإلغاء.",
    },
    'en': {
        'processing': "File received, processing...",
        'invalid': "The file must be in .webm format only.",
        'success': "Converted successfully!\nTime taken: {duration} seconds",
        'error': "An error occurred: {error}",
        'language_set': "Language changed to English.",
        'choose_lang': "Choose your language:",
        'settings': "⚙️ Settings",
        'cancel': "Cancel",
        'change_token': "Change Token",
        'settings_info': "⚙️ Settings:\n\nCurrent bot token:\n`{token}`\n\nDo you want to change the token?",
        'ask_new_token': "Send the new token now:",
        'token_updated': "Token updated successfully! ✅",
        'token_invalid': "Invalid token! Please try again.",
        'cancelled': "Cancelled.",
    }
}

def get_lang(user_id):
    return user_languages.get(str(user_id), 'ar')

# بداية البوت
TOKEN = get_bot_token()
bot = telebot.TeleBot(TOKEN)

# -- دوال التعامل مع اللغة --
@bot.message_handler(commands=['start', 'lang'])
def send_language_buttons(message):
    lang = get_lang(message.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("العربية", callback_data='lang_ar'),
        InlineKeyboardButton("English", callback_data='lang_en')
    )
    # إذا تم تفعيل خيار "لا تسألني" نضيف زر الإعدادات
    config = load_config()
    if config.get("skip_token_prompt", False):
        markup.add(InlineKeyboardButton(messages[lang]['settings'], callback_data='settings'))
    bot.send_message(message.chat.id, messages[lang]['choose_lang'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_') or call.data in ['settings', 'change_token', 'cancel_token'])
def handle_callback(call):
    user_id = str(call.from_user.id)
    lang = get_lang(user_id)

    if call.data.startswith('lang_'):
        lang_code = call.data.split('_')[1]
        user_languages[user_id] = lang_code
        save_languages()
        bot.edit_message_text(
            messages[lang_code]['language_set'],
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        return

    if call.data == 'settings':
        # عرض التوكن الحالي وخيارات التعديل
        with open(TOKEN_FILE, "r") as f:
            current_token = f.read().strip()
        text = messages[lang]['settings_info'].format(token=current_token)
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(messages[lang]['change_token'], callback_data='change_token'),
            InlineKeyboardButton(messages[lang]['cancel'], callback_data='cancel_token')
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data == 'change_token':
        msg = bot.send_message(call.message.chat.id, messages[lang]['ask_new_token'])
        bot.register_next_step_handler(msg, process_new_token)
        return

    if call.data == 'cancel_token':
        bot.send_message(call.message.chat.id, messages[lang]['cancelled'])
        return

def process_new_token(message):
    global bot
    lang = get_lang(str(message.from_user.id))
    new_token = message.text.strip()

    if not new_token or ' ' in new_token:
        bot.send_message(message.chat.id, messages[lang]['token_invalid'])
        bot.register_next_step_handler(message, process_new_token)
        return

    with open(TOKEN_FILE, "w") as f:
        f.write(new_token)

    bot.send_message(message.chat.id, messages[lang]['token_updated'])
    print(f"{Colors.OKGREEN}[+] Token updated successfully from settings! ✅{Colors.ENDC}")

    # إعادة تهيئة البوت بالتوكن الجديد
    bot = telebot.TeleBot(new_token)

# التعامل مع الملفات (webm to mp4 conversion)
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

# طباعة ASCII art مع رسالة بداية تشغيل البوت
ascii_art = """
⠀⠀
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
[•] VERSION   : 2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━
The script has been turned on the telegram bot
"""

print(ascii_art)

bot.polling()
