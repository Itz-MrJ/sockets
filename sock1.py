import socket,json,pickle,pymongo,dns,traceback
import threading
from selenium import webdriver

HEADER = 2048
PORT = 5001
SERVER = ''
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNEC"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def conmongo():
    global mycol,match,botv,withs,customb,supp,valomatch,valoteams
    mong = pymongo.MongoClient("mongodb+srv://MrJaguar:Aryaarunkumaristhebest@cluster0.qmhrz.mongodb.net/MrJtourneys?authSource=admin&retryWrites=true&w=majority")
    print("connected successfully")
    mycol = mong["MrJtourneys"]["UserData"]
    supp = mong["MrJtourneys"]["support"]
    match = mong["MrJtourneys"]["matches"]
    botv = mong['MrJtourneys']['verfbots']
    withs = mong['MrJtourneys']['withdrawals']
    customb = mong['MrJtourneys']['customBots']
    valomatch = mong['MrJtourneys']['valomatches']
    valoteams = mong['MrJtourneys']['valoteams']
    
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msg_length = conn.recv(HEADER)
    driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
    gg = pickle.loads(msg_length)
    test = driver.get(f"https://api.tracker.gg/api/v2/valorant/standard/matches/riot/{gg['valorant']}?type={gg['gamemode']}")
    try:
        data = json.loads(driver.find_element_by_tag_name('pre').text)
        attrid = data['data']['matches'][0]['attributes']['id']
        print(attrid)
        if gg['last']!=str(attrid):
            kk = 5
            if gg['gamemode']=="competitive":
                kk=0
            if gg['gamemode']=="unrated":
                kk=1
            if gg['gamemode']=="deathmatch":
                kk=2
            if kk==5:
                return
            for i in mycol.find({'displayName': gg['displayName']}):
                if str(attrid) != i['royales'][kk]:
                    if data['data']['matches'][0]['metadata']['result'] == "defeat":
                        return
                    i['royales'][kk] = str(attrid)
                    mycol.update_one({'displayName': gg['displayName']},{"$set": {'royales': i['royales']}})
            for i in valomatch.find({'matchid': gg['matchid']}):
                try:
                    pp = 99
                    if kk==0:
                        pp = 3
                    if kk==1:
                        pp = 2
                    if kk==2:
                        pp = 1
                    if pp==99:
                        return
                    print(i['userData'][i['joinedUsersList'].index(gg['displayName'])]['user'])
                    if i['userData'][i['joinedUsersList'].index(gg['displayName'])]['user'] == gg['displayName']:
                        print('in updating')
                        i['userData'][i['joinedUsersList'].index(gg['displayName'])]['points'] += pp
                        valomatch.update_one({'matchid': gg['matchid']}, {"$set": {'userData': i['userData']}})
                    else:
                        print('in else')
                        kk = 0
                        while kk < len(i['userData']):
                            if i['userData'][kk]['displayName'] == gg['displayName']:
                                i['userData'][kk]['points'] += pp
                                valomatch.update_one({'matchid': gg['matchid']}, {"$set": {'userData': i['userData']}})
                                break
                            kk+=1
                except:
                    traceback.print_exc()
    except:
        print(json.loads(driver.find_element_by_tag_name('pre').text))
        if json.loads(driver.find_element_by_tag_name('pre').text)['errors'][0]['code']=="CollectorResultStatus::NotFound":
            mycol.update_one({'displayName':gg['displayName']}, {"$set": {'err': 'Your valorant id might have been changed. Please contact our support team to help you out with this issue.'}})
        if json.loads(driver.find_element_by_tag_name('pre').text)['errors'][0]['code']=="CollectorResultStatus::NoData":
            mycol.update_one({'displayName':gg['displayName']}, {"$set": {'err': 'No games played on your account to track.'}})
        if json.loads(driver.find_element_by_tag_name('pre').text)['errors'][0]['code']=="CollectorResultStatus::Private":
            mycol.update_one({'displayName':gg['displayName']}, {"$set": {'err': 'Your account is still private. Contact our support to fix this issue.'}})
    finally:
        conn.close()
            

def start():
    conmongo()
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
