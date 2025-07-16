from sma_sunnyboy import WebConnect, Key, Right
# from machine import Pin, I2C

address = "my_ipaddr"
password = "my_pw"
right = Right.USER

# i2c = I2C(0, scl=Pin(17), sda=Pin(16))
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Création de l'objet WebConnect
client = WebConnect(address, right, password)

# Authentification
client.auth()

# Vérification de la connexion
if not client.check_connection():
    print("[/!\\] Connexion impossible, revérifie SVP")
else:
    print("[+] Connecté au SMA Sunny Boy 5.0 de Bruno")
    print("[*] --------------------------------------")

# Production instantanée
    power_current = client.get_value(Key.power_current)
    print("Puissance prod.: %d%s" % (power_current, Key.power_current["unit"]))

# Production totale
    power_total = client.get_value(Key.power_total)
    print("Prod. tot.: %d%s" % (power_total, Key.power_total["unit"]))

# Partie réseau
    ethernet_ip = client.get_value(Key.ethernet_ip)
    ethernet_netmask = client.get_value(Key.ethernet_netmask)
    print("@IP_Onduleur: %s / Masque: %s " % (ethernet_ip,ethernet_netmask))
    
# Temps de service
    service_time = client.get_value(Key.service_time)
    print(f"Temps de service: {service_time/3600:.3f} heures ou {service_time/3600/24/365:.6f} années")

# Durée d'injection
    injection_time = client.get_value(Key.injection_time)
    print(f"Temps d’injection: {injection_time/3600:.3f} heures ou {injection_time/3600/24/365:.6f} années")

    print("[+] Déconnexion..")
    if client.logout() is False:
        print("[!] Erreur dans la déconnexion!")
    print("[+] Terminé.")
    
# oled.fill(0)
# oled.text("Prod. inst:", 0, 0)
# oled.text(str(power_current) + " W", 0, 10)
# oled.text("Total jour:", 0, 30)
# oled.text(str(power_total) + " W", 0, 40)
# oled.show()