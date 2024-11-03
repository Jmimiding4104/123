from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# 機器人的 Token
TOKEN = "8174698910:AAHN3yvUjtGReFUVMTNUNP3C_B-XoHyVYKE"

# 定義 /start 指令的回應
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """當用戶發送 /start 命令時的處理函數"""
    await update.message.reply_text('歡迎使用翻譯機器人! 直接發送文字給我來進行翻譯。')

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    try:
        text = update.message.text
        
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair=zh|en"
        else:
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|zh"
            
        response = requests.get(url).json()
        translation = response['responseData']['translatedText']
        await update.message.reply_text(f"原文: {text}\n翻譯: {translation}")
        
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("翻譯錯誤，請稍後再試")

# 主程式
def main():
    # 初始化應用程式
    app = Application.builder().token(TOKEN).build()

    # 新增 /start 指令的處理器
    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    # 啟動機器人
    app.run_polling()

if __name__ == "__main__":
    main()