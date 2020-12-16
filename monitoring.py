#Simple Monitoring by Lonov
import socket,requests,time,os,threading,urllib

minecraft="mc.example.com" #TODO Minecraft ping
mysql="" #TODO Mysql check
site="http://127.0.0.1"
vk_token="token"
vk_peer_id=""



mc_downs=0
mysql_downs=0
site_downs=0


def alert(msg):
    print("\n [!]"+(msg))
    try:
         requests.get("https://api.vk.com/method/messages.send?access_token="+vk_token+"&v=5.86f&peer_id="+vk_peer_id+"&message={}".format(msg))
    except:
            print("vk err")

def reseter():
    global mc_downs, site_downs
    while True:
        alert("Downs today: <br><br> MC: {} <br> Site: {}".format(mc_downs,site_downs))
        mc_downs=0
        mysql_downs=0
        site_downs=0
        
        time.sleep(86400) #24 ч
        
def tcp(host,port): #TODO Minecraft Ping 
    s=socket.socket()
    s.settimeout(3)
    try:
        s.connect((host,port))
        res=1
        s.close()
    except:
    	s.close()
    	res=0
    return res

def http(url):
    try:
        if requests.get(url, verify=False, timeout=10).status_code == 200:
               res=1
        else:
            res=0
    except:
        res=0
    return res

threading.Thread(target=reseter).start()

while True:
    print("Checking started...")
    online=0
    stext="[MONITORING ALERT]<br><br>"
	#mc
    if tcp(minecraft,25565) == 1:
        stext+="MC: OK<br>"
        online+=1
    else:
        stext+="MC: FAILED<br>"
        mc_downs+=1
	#http
    if http(site) == 1:
        stext+="Site: OK<br>"
        online+=1
    else:
        stext+="Site: FAILED<br>"
        site_downs+=1
		
	#gen results
    if online != 2:
        alert(stext)
	
    time.sleep(600)

