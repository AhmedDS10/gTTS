#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكربت لتحويل النص العربي إلى ملف صوتي
"""

from gtts import gTTS
import os
import argparse

def text_to_speech(text, output_file="output.mp3", language="ar", slow=False):
    """
    تحويل النص إلى صوت باستخدام Google Text-to-Speech API
    
    المعاملات:
        text (str): النص المراد تحويله إلى صوت
        output_file (str): اسم ملف الصوت الناتج
        language (str): رمز اللغة ('ar' للعربية)
        slow (bool): إبطاء سرعة النطق
        
    تُرجع:
        str: مسار ملف الصوت الناتج
    """
    try:
        # إنشاء كائن gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # حفظ الصوت في ملف
        tts.save(output_file)
        
        print(f"تم إنشاء ملف الصوت بنجاح: {output_file}")
        return output_file
    except Exception as e:
        print(f"حدث خطأ أثناء تحويل النص إلى صوت: {e}")
        return None

def play_sound(file_path):
    """
    تشغيل ملف الصوت باستخدام مشغل الصوت الافتراضي للنظام
    
    المعاملات:
        file_path (str): مسار ملف الصوت
    """
    try:
        # استخدم الأمر المناسب حسب نظام التشغيل
        if os.name == 'posix':  # لينكس/ماك
            os.system(f"xdg-open {file_path}")
        elif os.name == 'nt':  # ويندوز
            os.system(f"start {file_path}")
        else:
            print("لا يمكن تشغيل الملف تلقائيًا على نظام التشغيل هذا")
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل الصوت: {e}")

def main():
    parser = argparse.ArgumentParser(description="تحويل النص العربي إلى صوت")
    parser.add_argument("--text", "-t", help="النص المراد تحويله إلى صوت", type=str)
    parser.add_argument("--file", "-f", help="ملف نصي للتحويل", type=str)
    parser.add_argument("--output", "-o", help="اسم ملف الصوت الناتج", default="output.mp3", type=str)
    parser.add_argument("--lang", "-l", help="رمز اللغة (ar للعربية)", default="ar", type=str)
    parser.add_argument("--slow", "-s", help="إبطاء سرعة النطق", action="store_true")
    parser.add_argument("--play", "-p", help="تشغيل الصوت بعد الإنشاء", action="store_true")
    
    args = parser.parse_args()
    
    text = ""
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"حدث خطأ أثناء قراءة الملف: {e}")
            return
    else:
        print("يرجى إدخال نص باستخدام --text أو تحديد ملف باستخدام --file")
        return
    
    output_file = text_to_speech(text, args.output, args.lang, args.slow)
    
    if output_file and args.play:
        play_sound(output_file)

if __name__ == "__main__":
    main()
