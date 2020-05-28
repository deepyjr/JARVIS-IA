import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib


engine = pyttsx3.init()
wikipedia.set_lang("fr")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("Il est")
    speak(time)

def goodBye():
    speak("A tres bientot monsieur")

def date():
    year = int(datetime.datetime.now().year)
    month = datetime.datetime.now().strftime("%B")
    day = int(datetime.datetime.now().day)
    speak("Nous sommes le")
    engine.say(day)
    engine.say(month)
    engine.say(year)
    engine.runAndWait()
    
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Bonjour Monsieur! Vous revoila enfin! Quelle superbe Matinée!")
    elif hour >= 12 and hour < 18:
        speak("Bonjour Monsieur! Vous revoila enfin! Quelle superbe Après Midi!")
    elif hour >= 18 and hour <24 :
        speak("Bonsoir Monsieur! Vous revoila enfin! Quelle superbe Soirée!")
    else:
        speak("Bonsoir Monsieur ! Vous revoila enfin!")   

    time()
    date()
    speak("Jarvisse a votre service. Que puis-je faire pour vous ?")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('assistant.deepyjr@gmail.com', 'Assistant34&*')
    server.sendmail('deepyjr@gmail.com',to,content)
    server.close()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("En écoute..")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("J'analyse la demande..")
        query = r.recognize_google(audio, language='fr-fr')
        print(query)
    except Exception as e:
        print(e)
        speak("Pouvez vous répéter s'il vous plait?")
        return("None")
    
    return query

if __name__ == "__main__":
    # wishMe()
    while True:
        query = takeCommand().lower()
        if 'heure' in query:
            time()
        elif 'date' in query:
            date()
        elif 'wikipédia' in query:
            speak("Recherche en cours..")
            query = query.replace("wikipédia","")
            result = wikipedia.summary(query,sentences=1)
            print(result)
            speak(result)
        elif 'rien' in query:
            goodBye()
            quit()
        elif 'arrête-toi' in query:
            goodBye()
            quit()
        elif 'déconnecte-toi' in query:
            goodBye()
            quit()
        elif 'offline' in query:
            goodBye()
            quit()
        elif 'mail' in query:
            try:
                speak("Que dois-je envoyer comme contenu ?")
                content = takeCommand()

                speak("A qui dois-je envoyer votre mail ?")
                to = takeCommand().lower()

                if 'margaux' in to:
                    to = 'margaux.le-roux@hotmail.com'
                elif 'moi' in to:
                    to = 'deepyjr@gmail.com'
                elif 'margot' in to:
                    to = 'margaux.le-roux@hotmail.com'


                sendEmail(to, content)
                speak("Votre mail a bien été envoyé Monsieur!")
            except Exception as e:
                print(e)
                speak("L'envoie de votre mail a échoué")