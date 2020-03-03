# import pyttsx3
# engine = pyttsx3.init()
# engine.say("Ксюша я тебя люблю")
# engine.runAndWait()


# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
#


import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))




# query = r.recognize_google(audio, language='ru-RU')
# print('You said:' + query.lower())

#
#
#
# import os
# import time
# import speech_recognition as sr
# from fuzzywuzzy import fuzz
# import pyttsx3
# import datetime
#
# # настройки
# opts = {
#     "alias": ('Xenia'),
#     "tbr": ('tell me', 'say', 'how much', 'how many'),
#     "cmds": {
#         "ctime": ('time', 'time now', 'which time'),
#         "radio": ('turn the music on', 'turn on the radio', 'turn on music'),
#         "stupid1": ('tell me something', 'make me laugh', 'do you know something interesting')
#     }
# }
#
#
# # функции
# def speak(what):
#     print(what)
#     speak_engine.say(what)
#     speak_engine.runAndWait()
#     speak_engine.stop()
#
#
# def callback(recognizer, audio):
#     try:
#         voice = recognizer.recognize_google(audio).lower()
#         print("[log] You said: " + voice)
#
#         if voice.startswith(opts["alias"]):
#             # обращаются к Ксюше
#             cmd = voice
#
#             for x in opts['alias']:
#                 cmd = cmd.replace(x, "").strip()
#
#             for x in opts['tbr']:
#                 cmd = cmd.replace(x, "").strip()
#
#             # распознаем и выполняем команду
#             cmd = recognize_cmd(cmd)
#             execute_cmd(cmd['cmd'])
#
#     except sr.UnknownValueError:
#         print("[log] The voice unsupposed!")
#     except sr.RequestError as e:
#         print("[log] Some internet error!")
#
#
# def recognize_cmd(cmd):
#     RC = {'cmd': '', 'percent': 0}
#     for c, v in opts['cmds'].items():
#
#         for x in v:
#             vrt = fuzz.ratio(cmd, x)
#             if vrt > RC['percent']:
#                 RC['cmd'] = c
#                 RC['percent'] = vrt
#
#     return RC
#
#
# def execute_cmd(cmd):
#     if cmd == 'ctime':
#         # сказать текущее время
#         now = datetime.datetime.now()
#         speak("Now " + str(now.hour) + ":" + str(now.minute))
#
#     elif cmd == 'radio':
#         # воспроизвести радио
#         #os.system("D:\\Jarvis\\res\\radio_record.m3u")
#         pass
#
#     elif cmd == 'stupid1':
#         # рассказать анекдот
#         speak("there are no interesting things")
#
#     else:
#         print('Repeat please!')
#
#
# # запуск
# r = sr.Recognizer()
# m = sr.Microphone(device_index=0)
#
# with m as source:
#     r.adjust_for_ambient_noise(source)  # Cлушаем шум для того чтобы различать голос человека от шума
#
# speak_engine = pyttsx3.init()
#
#
# # forced cmd test
#
# speak("Hello, Alex")
# speak("Xenia hearing")
#
# stop_listening = r.listen_in_background(m, callback)
# while  True: time.sleep(0.1) # infinity loop