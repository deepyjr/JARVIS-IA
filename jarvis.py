import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import requests



engine = pyttsx3.init()
wikipedia.set_lang("fr")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def connectedToday(date):
    remember = open('log.txt','r')
    logData = remember.read()
    if date == logData:
        speak("Vous revoilà Professeur, vous m'aviez manqué. Que puis-je faire pour vous ?")
    else:
        wishMe()

def writeLog(day,month):
    reminder = open('log.txt','w')
    reminder.write(str(day) +''+ str(month))
    reminder.close()
    date = str(day)+''+str(month)
    return date
 
def time():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("Il est")
    speak(time)

def goodBye():
    speak("A tres bientot Professeur")

def dateData():
    yearDate = int(datetime.datetime.now().year)
    monthDate = datetime.datetime.now().strftime("%B")
    dayDate = int(datetime.datetime.now().day)
    speak("Nous sommes le")
    engine.say(dayDate)
    engine.say(monthDate)
    engine.say(yearDate)
    engine.runAndWait()
    
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Bonjour Professeur! Vous revoila enfin! Quelle superbe Matinée!")
    elif hour >= 12 and hour < 18:
        speak("Bonjour Professeur! Vous revoila enfin! Quelle superbe Après Midi!")
    elif hour >= 18 and hour <24 :
        speak("Bonsoir Professeur! Vous revoila enfin! Quelle superbe Soirée!")
    else:
        speak("Bonsoir Professeur ! Vous revoila enfin!")   

    time()
    dateData()
    speak("Jarvisse a votre service. Que puis-je faire pour vous ?")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('assistant.deepyjr@gmail.com', 'Assistant34&*')
    server.sendmail('deepyjr@gmail.com',to,content)
    server.close()

def weather(day):

    dayStr = str(day)
    url="https://api.meteo-concept.com/api/forecast/daily/"+dayStr+"?token=8c1dde9d98336d26a62f2e8969c794f716c77776fd3d171b431881ea4d6e9252&insee=78123"
    content=requests.get(url)
    dataWeather=content.json()
    return dataWeather

def dailyWeatherCheck(dataWeather):
    tmin = str(dataWeather['forecast']['tmin'])
    tmax = str(dataWeather['forecast']['tmax'])
    rainProb = str(dataWeather['forecast']['probarain'])
    frostProb = str(dataWeather['forecast']['probafrost'])
    totalRain = str(dataWeather['forecast']['rr1'])

    if int(tmin) < 15 and int(frostProb):
        speak("Il fera au minimum"+tmin+"degrés et au maximum"+tmax+"degrés, avec une probabilité de pluie de "+rainProb+"% et un risque de gel de"+frostProb)
    if int(rainProb)>=50:
        speak("Il fera au minimum"+tmin+"degrés et au maximum"+tmax+"degrés, avec une probabilité de pluie de "+rainProb+"% il est prévu en tout"+totalRain+"millimètres cumulé sur la journée. Vous devriez penser a prendre un parapluie si vous sortez")
    else:
        speak("Il fera au minimum"+tmin+"degrés et au maximum"+tmax+"degrés, avec une probabilité de pluie de "+rainProb+"%")


def averageWeather():
    averageTmin =[]
    averageTmax = []
    averageRainProb=[]
    averageFrostProb=[]
    
    for i in range(0,3):
        i = str(i)
        url="https://api.meteo-concept.com/api/forecast/daily/"+i+"?token=8c1dde9d98336d26a62f2e8969c794f716c77776fd3d171b431881ea4d6e9252&insee=78123"
        content=requests.get(url)
        dataWeather=content.json()
        tmin = dataWeather['forecast']['tmin']
        tmax = dataWeather['forecast']['tmax']
        rainProb = dataWeather['forecast']['probarain']
        frostProb = dataWeather['forecast']['probafrost']
        
        averageTmin.append(tmin)
        averageTmax.append(tmax)
        averageRainProb.append(rainProb)
        averageFrostProb.append(frostProb)
    
    averageTmin = str(moyenne(averageTmin))
    averageTmax = str(moyenne(averageTmax))
    averageRainProb= str(moyenne(averageRainProb))
    averageFrostProb= str(moyenne(averageFrostProb))
        
    speak("Il fera en moyenne sur les 3 prochains jours au minimum"+averageTmin+" degrés et au maximum"+averageTmax+"degrés. La probabilité d'une pluie est de"+ averageRainProb+"% avec une probabilité de neige de "+averageFrostProb+"%") 

def moyenne(liste):
    return round(sum(liste)/len(liste))


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

def offMod():
    speak("Je repasse en veille, j'espère vous revoir vite.")

def startStat():
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
        return("Aucune commande pour l'instant")
    
    return query

if __name__ == "__main__":
    while True:
        start = startStat().lower()

        if 'ok jarvis' in start:

            # take the date and create a log 
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            date = writeLog(day, month)
            connectedToday(date)

            # wishMe()
            while True:

                query = takeCommand().lower()

                if 'heure' in query:
                    time()
                    offMod()
                    break

                elif 'date' in query:
                    dateData()
                    offMod()
                    break

                elif 'wikipédia' in query or 'Wikipédia' in query :
                    speak("Que dois-je rechercher ? Ne me donnez que le mot clé !")
                    content = takeCommand()
                    speak("Vous confirmez que je dois rechercher"+content)
                    answ = takeCommand().lower()
                    if 'oui' in answ:
                        speak("Recherche en cours..")
                        result = wikipedia.summary(content,sentences=1)
                        print(result)
                        speak(result)
                        offMod()
                        break
                    else:
                        speak("Votre recherche a échoué redemandez un envoie")

                elif 'météo' in query:
                    speak("Voulez vous la météo pour aujourd'hui ou pour demain ? Si vous désirez un cumule sur les 3 prochains jours dites moyenne sur 3 jours")
                    query = takeCommand().lower()

                    if "aujourd'hui" in query:
                        dailyWeatherCheck(weather(0))
                        offMod()
                        break

                    elif "demain" in query:
                        dailyWeatherCheck(weather(1))
                        offMod()
                        break

                    elif "3 jours" in query:
                        averageWeather()
                        offMod()
                        break
                    else:
                        speak("Je suis désolé professeur, je n'ai pas compris la date voulue pour la météo, recommencez une demande de météo.")

                   
                elif 'mail' in query:
                    try:
                        speak("Que dois-je envoyer comme contenu ?")
                        content = takeCommand()

                        speak("A qui dois-je envoyer votre mail ?")
                        to = takeCommand().lower()

                        if 'margaux' in to or 'margot' in to:
                            to = 'margaux.le-roux@hotmail.com'
                        elif 'moi' in to or 'raphael' in to:
                            to = 'deepyjr@gmail.com'

                        sendEmail(to, content)
                        speak("Votre mail a bien été envoyé Professeur!")
                        offMod()
                        break
                    
                    except Exception as e:
                        print(e)
                        speak("L'envoie de votre mail a échoué redemandez un envoie")


                elif 'site web' in query:
                    speak("A quel site voulez vous accéder?")
                    chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                    search = takeCommand().lower()
                    wb.get(chromePath).open_new_tab(search+'.com')
                    offMod()
                    break

                elif 'google' in query or 'internet' in query:
                    speak("Que voulez vous que je cherche sur google?")
                    chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                    search = takeCommand().lower()
                    newSearch = search.replace(" ","+")
                    wb.get(chromePath).open_new_tab("google.com/search?q="+search)
                    offMod()
                    break

                elif 'enregistre' in query:
                    while True:
                        speak("Que voulez vous que je retiennes pour vous ?")
                        data = takeCommand()
                        speak("Vous voulez que je note"+data)
                        answer = takeCommand().lower()
                        if 'oui' in answer:
                            remember = open('data.txt','w')
                            remember.write(data)
                            remember.close()
                            offMod()
                            break
                            
                        else:
                            ("recommencez la mémorisation")
                    
                    break

                elif 'mémoire' in query:
                    remember = open('data.txt','r')
                    speak("Vous m'avez demander de me souvenir de ca"+remember.read())
                    offMod()
                    break

                elif 'ferme ma session' in query:
                    speak("êtes vous sure de vouloir fermer voter session")
                    answer = takeCommand().lower()
                    if 'oui' in answer:
                        goodBye()
                        os.system("shutdown -l")
                 
                    
                elif 'offline' in query or 'rien' in query or 'arrête-toi' in query or 'déconnecte-toi' in query:
                    goodBye()
                    quit()

                

