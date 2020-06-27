import requests
import datetime
import time
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# Gestore webhook
def gestore_webhook(payload_str):
    FILE_TOKEN = FOLDER+'/token.json'
    if os.path.isfile(FILE_TOKEN):
        file = open(file=FILE_TOKEN,mode="r",encoding="utf-8")
        dati_token = json.loads(file.read(),encoding="utf-8")
        file.close()
    else:
        sys.exit("No tokenfile, aborting")
    
    WEBHOOK = dati_token["discord_webhook"]

    # Spara su discord
    req = requests.post(url=WEBHOOK,data={"content":payload_str})
    print(payload_str)


# Estrattore generico
def estrai_dati_sommari():
    # Thunderskill api
    # Non usata
    #API = "https://thunderskill.com/en/squad/-ITAR-/export/json"

    # Sito squadriglia
    SITO_SQUADRIGLIA = "https://warthunder.com/en/community/claninfo/SQUADRIGLIA%20ITALIANA%20ARIETI"

    # Cartella
    CARTELLA = "./Dati/"
    if not os.path.isdir(CARTELLA):
        os.mkdir(CARTELLA)

    # Dati
    dati = dict()
    FILE_DATI = CARTELLA+'/dati.json'
    if os.path.isfile(FILE_DATI):
        file = open(file=FILE_DATI,mode="r",encoding="utf-8")
        dati = json.loads(file.read(),encoding="utf-8")
        file.close()
    else:
        dati["membri"] = dict()
        dati["squadrone"] = "-ITAR-"
        dati["timestamp_precedente"] = str(datetime.datetime.now())
        dati["timestamp"] = dati["timestamp_precedente"]
        file = open(file=FILE_DATI,mode="w",encoding="utf-8")
        file.write(json.dumps(dati,indent=4,sort_keys=True))
        file.close()

    # Inizializza variabili
    member_links = dict()
    memberdict = dict()
    
    # Prendi i dati
    squadronpage = requests.get(url=SITO_SQUADRIGLIA)
    squadronsoup = BeautifulSoup(squadronpage.content,"html.parser")
    #table class="clan-members"
    memberlist = squadronsoup.find("table",class_="clan-members")
    memberlinks = memberlist.find_all("a")
    for memberlink in memberlinks:
        if "en/community/userinfo/?nick=" in memberlink["href"]:
            member_links[memberlink.get_text()] = "https://warthunder.com/"+memberlink["href"]

    # Controllo sommario
    # Tira su l'emulatore
    driver = webdriver.Firefox()

    try:
        for member in member_links:
            print(member)
            # Inizializza il dizionario
            memberdict[member] = dict()
            memberdict[member]["ab"] = dict()
            memberdict[member]["ab"]["air"] = dict()
            memberdict[member]["ab"]["air"]["battles"] = list()
            memberdict[member]["ab"]["ground"] = dict()
            memberdict[member]["ab"]["ground"]["battles"] = list()
            memberdict[member]["ab"]["sea"] = dict()
            memberdict[member]["ab"]["sea"]["battles"] = list()
            memberdict[member]["rb"] = dict()
            memberdict[member]["rb"]["air"] = dict()
            memberdict[member]["rb"]["air"]["battles"] = list()
            memberdict[member]["rb"]["ground"] = dict()
            memberdict[member]["rb"]["ground"]["battles"] = list()
            memberdict[member]["rb"]["sea"] = dict()
            memberdict[member]["rb"]["sea"]["battles"] = list()
            memberdict[member]["sb"] = dict()
            memberdict[member]["sb"]["air"] = dict()
            memberdict[member]["sb"]["air"]["battles"] = list()
            memberdict[member]["sb"]["ground"] = dict()
            memberdict[member]["sb"]["ground"]["battles"] = list()
            memberdict[member]["sb"]["sea"] = dict()
            memberdict[member]["sb"]["sea"]["battles"] = list()

            # Estrai i dati
            memberpage = driver.get(url=member_links[member])
            #ul class="profile-rate__fightType-list"
            buttonlist = WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH, '//ul[@class="profile-rate__fightType-list"]')))
            
            #ul class="profile-stat__list"
            stat_page = driver.page_source
            stat_soup = BeautifulSoup(stat_page,"html.parser")
            stat_container = stat_soup.find("div",class_="user-profile__stat profile-stat")
            stat_list = stat_container.findAll("div",class_="profile-stat__list-row")

            air_stats_container = stat_list[0]
            ground_stats_container = stat_list[1]
            sea_stats_container = stat_list[2]
            
            # Dati aerei
            air_stats_header = air_stats_container.find("ul",class_="profile-stat__list")
            air_stats_header_list = air_stats_header.findAll("li",class_="profile-stat__list-item")
            air_stats_ab = air_stats_container.find("ul",class_="profile-stat__list-ab")
            air_stats_ab_list = air_stats_ab.findAll("li",class_="profile-stat__list-item")
            air_stats_rb = air_stats_container.find("ul",class_="profile-stat__list-rb")
            air_stats_rb_list = air_stats_rb.findAll("li",class_="profile-stat__list-item")
            air_stats_sb = air_stats_container.find("ul",class_="profile-stat__list-sb")
            air_stats_sb_list = air_stats_sb.findAll("li",class_="profile-stat__list-item")
            for index in range(len(air_stats_header_list)):
                if air_stats_header_list[index].get_text().strip().lower() != "statistics":
                    memberdict[member]["ab"]["air"][air_stats_header_list[index].get_text().strip()] = air_stats_ab_list[index].get_text().strip()
                    memberdict[member]["rb"]["air"][air_stats_header_list[index].get_text().strip()] = air_stats_rb_list[index].get_text().strip()
                    memberdict[member]["sb"]["air"][air_stats_header_list[index].get_text().strip()] = air_stats_sb_list[index].get_text().strip()

            # Dati terrestri
            ground_stats_header = ground_stats_container.find("ul",class_="profile-stat__list")
            ground_stats_header_list = ground_stats_header.findAll("li",class_="profile-stat__list-item")
            ground_stats_ab = ground_stats_container.find("ul",class_="profile-stat__list-ab")
            ground_stats_ab_list = ground_stats_ab.findAll("li",class_="profile-stat__list-item")
            ground_stats_rb = ground_stats_container.find("ul",class_="profile-stat__list-rb")
            ground_stats_rb_list = ground_stats_rb.findAll("li",class_="profile-stat__list-item")
            ground_stats_sb = ground_stats_container.find("ul",class_="profile-stat__list-sb")
            ground_stats_sb_list = ground_stats_sb.findAll("li",class_="profile-stat__list-item")
            for index in range(len(ground_stats_header_list)):
                if ground_stats_header_list[index].get_text().strip().lower() != "statistics":
                    memberdict[member]["ab"]["ground"][ground_stats_header_list[index].get_text().strip()] = ground_stats_ab_list[index].get_text().strip()
                    memberdict[member]["rb"]["ground"][ground_stats_header_list[index].get_text().strip()] = ground_stats_rb_list[index].get_text().strip()
                    memberdict[member]["sb"]["ground"][ground_stats_header_list[index].get_text().strip()] = ground_stats_sb_list[index].get_text().strip()

            # Dati navali
            sea_stats_header = sea_stats_container.find("ul",class_="profile-stat__list")
            sea_stats_header_list = sea_stats_header.findAll("li",class_="profile-stat__list-item")
            sea_stats_ab = sea_stats_container.find("ul",class_="profile-stat__list-ab")
            sea_stats_ab_list = sea_stats_ab.findAll("li",class_="profile-stat__list-item")
            sea_stats_rb = sea_stats_container.find("ul",class_="profile-stat__list-rb")
            sea_stats_rb_list = sea_stats_rb.findAll("li",class_="profile-stat__list-item")
            sea_stats_sb = sea_stats_container.find("ul",class_="profile-stat__list-sb")
            sea_stats_sb_list = sea_stats_sb.findAll("li",class_="profile-stat__list-item")
            for index in range(len(sea_stats_header_list)):
                if sea_stats_header_list[index].get_text().strip().lower() != "statistics":
                    memberdict[member]["ab"]["sea"][sea_stats_header_list[index].get_text().strip()] = sea_stats_ab_list[index].get_text().strip()
                    memberdict[member]["rb"]["sea"][sea_stats_header_list[index].get_text().strip()] = sea_stats_rb_list[index].get_text().strip()
                    memberdict[member]["sb"]["sea"][sea_stats_header_list[index].get_text().strip()] = sea_stats_sb_list[index].get_text().strip()

    finally:
        # Tira giù l'emulatore
        driver.close()

    # Parsing dei dati sommari
    controldict = dict()
    newmemberlist = list()
    meritdict = dict()
    meritdict["all"]["most_battles"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["all"]["most_victories"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["all"]["most_kills"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["all"]["most_time"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["air"]["most_battles"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["air"]["most_victories"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["air"]["most_kills"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["air"]["most_time"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["ground"]["most_battles"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["ground"]["most_victories"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["ground"]["most_kills"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["ground"]["most_time"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["sea"]["most_battles"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["sea"]["most_victories"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["sea"]["most_kills"] = {["nome"]="Nessuno!";["valore"]=0}
    meritdict["sea"]["most_time"] = {["nome"]="Nessuno!";["valore"]=0}

    # Supporto a validazione
    def validate(element):
        if element.isdigit():
            return int(element)
        else:
            return 0
    
    for member in memberdict:
        # Valori di controllo
        # Meriti
        air_realistic_battles = validate(str(memberdict[member]["rb"]["air"]["Air battles"]))
        air_realistic_battles_victories = validate(str(memberdict[member]["rb"]["air"]["Air battles"]))
        air_realistic_battles_kills = validate(str(memberdict[member]["rb"]["air"]["Total targets destroyed"]))
        air_realistic_battles_time = validate(str(memberdict[member]["rb"]["air"]["Air battles"]))
        ground_realistic_battles = validate(str(memberdict[member]["rb"]["ground"]["Ground battles"]))
        sea_realistic_battles = validate(str(memberdict[member]["rb"]["sea"]["Naval battles"]))
        # Demeriti
        air_arcade_battles = validate(str(memberdict[member]["ab"]["air"]["Air battles"]))
        ground_arcade_battles = validate(str(memberdict[member]["ab"]["ground"]["Ground battles"]))
        sea_arcade_battles = validate(str(memberdict[member]["ab"]["sea"]["Naval battles"]))

        # Se non nei dati, tira dentro
        if not member in dati["membri"]:
            dati["membri"][member] = memberdict[member]
            newmemberlist.append(member)

        # Valori di confronto
        # Meriti
        old_air_realistic_battles = validate(str(dati[member]["rb"]["air"]["Air battles"]))
        old_ground_realistic_battles = validate(str(dati[member]["rb"]["ground"]["Ground battles"]))
        old_sea_realistic_battles = validate(str(dati[member]["rb"]["sea"]["Naval battles"]))
        # Demeriti
        old_air_arcade_battles = validate(str(dati["membri"][member]["ab"]["air"]["Air battles"]))
        old_ground_arcade_battles = validate(str(dati["membri"][member]["ab"]["ground"]["Ground battles"]))
        old_sea_arcade_battles = validate(str(dati["membri"][member]["ab"]["sea"]["Naval battles"]))
        
        # Controlli per meriti
        if air_
        
        # Controlli per le arcade
        if air_arcade_battles > old_air_arcade_battles:
            if member not in controldict:
                controldict[member] = dict()
            controldict[member]["air"] = air_arcade_battles-old_air_arcade_battles
            #contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(air_arcade_battles-old_air_arcade_battles)+" partite aeree in arcade dall'ultimo controllo\n"
        if ground_arcade_battles > old_ground_arcade_battles:
            if member not in controldict:
                controldict[member] = dict()
            controldict[member]["ground"] = ground_arcade_battles-old_ground_arcade_battles
            #contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(ground_arcade_battles-old_ground_arcade_battles)+" partite terrestri in arcade dall'ultimo controllo\n"
        if sea_arcade_battles > old_sea_arcade_battles:
            if member not in controldict:
                controldict[member] = dict()
            controldict[member]["sea"] = sea_arcade_battles-old_sea_arcade_battles
            #contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(sea_arcade_battles-old_sea_arcade_battles)+" partite navali in arcade dall'ultimo controllo\n"
        
        # Aggiorna i dati
        dati["membri"][member] = memberdict[member]
    
    # Crea la stringa
    contentstr = "Controllo periodico\n"
    contentstr = contentstr + "============\n"
    contentstr = contentstr + "Ultimo controllo: " + dati["timestamp"] + "\n"
    contentstr = contentstr + "============\n"

    # Nuovi membri
    contentstr = contentstr + "Nuovi Arrivi\n"
    for member in newmemberlist:
        contentstr = contentstr + "Benvenuto al giocatore "+member+" nella squadriglia!\n"
    if len(newmemberlist) == 0:
        contentstr = contentstr + "Nessun nuovo membro in questo periodo\n"
    contentstr = contentstr + "============\n"

    # Lista meriti
    contentstr = contentstr + "Lista Meriti\n"
    contentstr = contentstr + "Globale\n"
    contentstr = contentstr + "Più partite: "+""+"\n"
    contentstr = contentstr + "Più vittorie: "+""+"\n"
    contentstr = contentstr + "Più uccisioni: "+""+"\n"
    contentstr = contentstr + "Più tempo in partita: "+""+"\n"
    contentstr = contentstr + "Aria\n"
    contentstr = contentstr + "Più partite: "+""+"\n"
    contentstr = contentstr + "Più vittorie: "+""+"\n"
    contentstr = contentstr + "Più uccisioni: "+""+"\n"
    contentstr = contentstr + "Più tempo in partita: "+""+"\n"
    contentstr = contentstr + "Terra\n"
    contentstr = contentstr + "Più partite: "+""+"\n"
    contentstr = contentstr + "Più vittorie: "+""+"\n"
    contentstr = contentstr + "Più uccisioni: "+""+"\n"
    contentstr = contentstr + "Più tempo in partita: "+""+"\n"
    contentstr = contentstr + "Mare\n"
    contentstr = contentstr + "Più partite: "+""+"\n"
    contentstr = contentstr + "Più vittorie: "+""+"\n"
    contentstr = contentstr + "Più uccisioni: "+""+"\n"
    contentstr = contentstr + "Più tempo in partita: "+""+"\n"
    contentstr = contentstr + "============\n"

    # Lista arcade
    contentstr = contentstr + "Lista Disciplinare\n"
    for member in controldict:
        if "air" in controldict[member]:
            contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(controldict[member]["air"])+" partite aeree in arcade dall'ultimo controllo\n"
        if "ground" in controldict[member]:
            contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(controldict[member]["ground"])+" partite terrestri in arcade dall'ultimo controllo\n"
        if "sea" in controldict[member]:
            contentstr = contentstr + "Il giocatore "+member+" ha effettuato "+str(controldict[member]["sea"])+" partite navali in arcade dall'ultimo controllo\n"
    if len(controldict) == 0:
        contentstr = contentstr + "Nessuna nuova partita arcade in questo periodo\n"
        
    contentstr = contentstr + "============"

    # Back up dei vecchi dati
    #file1 = open(file=FILE_DATI,mode="r",encoding="utf-8")
    #file2 = open(file=FILE_DATI+".old",mode="w",encoding="utf-8")
    #file2.write(file1.read())
    #file1.close()
    #file2.close()

    # Aggiornamento timestamp
    dati["timestamp_precedente"] = dati["timestamp"]
    dati["timestamp"] = str(datetime.datetime.now())
    
    # Salva su file
    #file = open(file=FILE_DATI,mode="w",encoding="utf-8")
    #file.write(json.dumps(dati,indent=4,sort_keys=True))
    #file.close()

    # Incarta tutto
    _dati_sommari = dict()
    _dati_sommari["controllo"] = controldict
    _dati_sommari["stringa"] = contentstr
    _dati_sommari["dati"] = dati
        
    return _dati_sommari


# Estrattore puntuale
def estrai_dati_precisi(utenti):
    # War thunder replays
    WT_USR = "Aries_B"
    WT_EMAIL = "alexsandftw@gmail.com"
    WT_PWD = "aries_bot"
    WT_LOGIN = "https://login.gaijin.net/en/"
    WT_REPLAY = "https://warthunder.com/en/tournament/replay/"

    # Controllo ad personam
    # Tira su l'emulatore
    driver = webdriver.Firefox()

    try:
        # Log in su warthunder
        loginpage = driver.get(url=WT_LOGIN)
        # input id="email" class="js-login-field form-input"
        # input id="password" class="form-input js-password-field"
        # input class="submit js-anti-several-clicks btn personal-account btn-blue"
        emailfield = WebDriverWait(driver,120).until(EC.presence_of_element_located((By.ID, 'email')))
        passwordfield = WebDriverWait(driver,120).until(EC.presence_of_element_located((By.ID, 'password')))
        submitbutton = WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="submit js-anti-several-clicks btn personal-account btn-blue"]')))

        emailfield.send_keys(WT_EMAIL)
        passwordfield.send_keys(WT_PWD)
        ActionChains(driver).click(submitbutton).perform()

        # Wait for account button
        accountbutton = WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="list-group-item auth-link auth-link--caret"]')))
        ActionChains(driver).click(accountbutton).perform()

        # Wait for log in
        WebDriverWait(driver,120).until(EC.text_to_be_present_in_element((By.XPATH,'//div[@class="section-name"]')," — Security settings for "+WT_USR+" ("+WT_EMAIL+")"))

        # Try to enter the replay page
        replaypage = driver.get(WT_REPLAY)

        # Wait for security gate
        accountbutton = WebDriverWait(driver,120).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="list-group-item auth-link auth-link--caret"]')))
        ActionChains(driver).click(accountbutton).perform()

        # Welcome to the replay page
        # Finally
        # *Sob*

        # Wait to make sure
        findbutton = WebDriverWait(driver,120).until(EC.presence_of_element_located((By.XPATH,'//input[@class="btn replay__btn--find"]')))

        # Now for all flagged members
        for member in utenti:
            #https://warthunder.com/en/tournament/replay/type/replays?Filter%5Bnick%5D=NICK_HERE&action=search"
            # Try to enter the replay page
            #replaypage = driver.get(WT_REPLAY+"type/replays?Filter[statistic_group]=aircraft&Filter[game_mode][]=arcade&Filter[nick]="+member+"&action=search")
            #replaypage = driver.get(WT_REPLAY+"type/replays?Filter[statistic_group]=tank&Filter[game_mode][]=arcade&Filter[nick]="+member+"&action=search")
            replaypage = driver.get(WT_REPLAY+"type/replays?Filter[game_mode][]=arcade&Filter[nick]="+member+"&action=search")
            print(member)
            # Note 25 entries per page
        
        while True:
            pass
    finally:
        # Tira giù l'emulatore
        driver.close()


# Logica principale
# Messaggio di cortesia
#gestore_webhook("Avvio del bot")

# Primo passaggio
#dati_sommari = estrai_dati_sommari()

# Pubblicazione sommaria
#print(dati_sommari["stringa"])
#gestore_webhook(dati_sommari["stringa"])

# Secondo passaggio
#print(dati_sommari["controllo"])

lista_prova = list()
lista_prova.append("Marcvs101")
estrai_dati_precisi(lista_prova)

# Pubblicazione secondaria
#gestore_webhook(dati_puntuali["stringa"])


    
