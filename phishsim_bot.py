import telebot
import logging
from datetime import datetime

# === CONFIG ===
TOKEN = '7874812639:AAFHdiRmcBP89_TS9VIhnzy9Zc6pbpK2vxQ'  # Replace this with your actual bot token
bot = telebot.TeleBot(TOKEN)

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# === Step 1: Start ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "👋 Welcome to ScamSimBot!\n\n"
                                      "This is a safe and educational simulation.\n"
                                      "Type /simulate to see how scammers trick people.")

# === Step 2: Simulate Phishing Flow ===
@bot.message_handler(commands=['simulate'])
def handle_simulation(message):
    bot.send_message(message.chat.id, "🚨 Alert: We detected unauthorized activity on your bank card ending in ****.\n\n"
                                      "To protect your funds, please verify your card.")
    bot.send_message(message.chat.id, "🔒 Enter your 16-digit card number:")
    bot.register_next_step_handler(message, collect_card)

def collect_card(message):
    card_number = message.text.strip()
    user = message.from_user.username or f"id:{message.from_user.id}"
    logging.info(f"[{user}] Simulated card entered: {card_number}")
    bot.send_message(message.chat.id, "✅ Card accepted.\nA verification code was just sent via SMS.")
    bot.send_message(message.chat.id, "📩 Please enter the 6-digit code you received:")
    bot.register_next_step_handler(message, collect_otp)

def collect_otp(message):
    code = message.text.strip()
    user = message.from_user.username or f"id:{message.from_user.id}"
    logging.info(f"[{user}] Simulated OTP entered: {code}")

    bot.send_message(message.chat.id, "⛔ STOP! This was a simulation.")
    bot.send_message(message.chat.id, "👀 If this had been a real scam, your bank account could be empty now.")

    bot.send_message(message.chat.id, "🧠 Lesson:\n"
                                      "- Legit bots never ask for card numbers or OTP codes.\n"
                                      "- Always check the official website.\n"
                                      "- Think before you tap!")

    bot.send_message(message.chat.id, "📘 Want to test your knowledge? Type /quiz to take a quick anti-scam test.")

# === Step 3: Optional Quiz ===
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    question = "Which of these is a red flag for a scam?"
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("✅ A bot asks for your card number", "❌ A bot offers a reminder")
    bot.send_message(message.chat.id, question, reply_markup=markup)
    bot.register_next_step_handler(message, evaluate_quiz)

def evaluate_quiz(message):
    if "card number" in message.text.lower():
        bot.send_message(message.chat.id, "🎉 Correct! That’s a big red flag.")
    else:
        bot.send_message(message.chat.id, "⚠️ Actually, asking for a card number is a huge warning sign.")

    bot.send_message(message.chat.id, "Type /simulate to try again or /start to return to the beginning.")

# === Run Bot ===
print("🤖 ScamSimBot is running...")
bot.polling()
