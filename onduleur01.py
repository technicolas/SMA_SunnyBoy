import json
from sma_sunnyboy import WebConnect, Key, Right
from datetime import timedelta
# from machine import Pin, I2C

with open("config.json") as f:
    config = json.load(f)

address = config["address"]
password = config["password"]
right = getattr(Right, config.get("right", "USER"))

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
    print("SMA Sunny Boy 5.0")
    print(f"{'-'*17}")

# Production instantanée
    power_current = client.get_value(Key.power_current)
# Production totale
    power_total = client.get_value(Key.power_total)

    print("Puissance prod.: %d %s / Prod. tot.: %d %s" % (power_current, Key.power_current["unit"], power_total, Key.power_total["unit"]))

# Partie réseau
    ethernet_ip = client.get_value(Key.ethernet_ip)
    ethernet_netmask = client.get_value(Key.ethernet_netmask)
    print("@IP_Onduleur: %s / Masque: %s " % (ethernet_ip,ethernet_netmask))
    
# Temps de service
    def format_duration(seconds):
        delta = timedelta(seconds=seconds)
        total_days = delta.days
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return years, months, days, hours, minutes, seconds

    # Récupération des valeurs
    service_time = client.get_value(Key.service_time)
    injection_time = client.get_value(Key.injection_time)

    # Formatage (récupération du tableau des valeurs)
    service = format_duration(service_time)
    injection = format_duration(injection_time)

    # Affichage en tableau
    print(f"{'Type':<15} {'Années':<6} {'Mois':<5} {'Jours':<6} {'Heures':<7} {'Minutes':<8} {'Secondes':<9}")
    print(f"{'-'*61}")
    print(f"{'Service':<15} {service[0]:<6} {service[1]:<5} {service[2]:<6} {service[3]:<7} {service[4]:<8} {service[5]:<9}")
    print(f"{'Injection':<15} {injection[0]:<6} {injection[1]:<5} {injection[2]:<6} {injection[3]:<7} {injection[4]:<8} {injection[5]:<9}")


    print("[INFO] Déconnexion...")
    if client.logout() is False:
        print("[INFO] Erreur dans la déconnexion!")
    print("[INFO] OK.")
    
# oled.fill(0)
# oled.text("Prod. inst:", 0, 0)
# oled.text(str(power_current) + " W", 0, 10)
# oled.text("Total jour:", 0, 30)
# oled.text(str(power_total) + " W", 0, 40)
# oled.show()
