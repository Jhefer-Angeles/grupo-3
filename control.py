from datetime import datetime

print(f"fecha y hora: ¨{datetime.now()}")
print("controlo de automoviles:")
print("===============================")

import time
import os

GREN = "\033[32m"
END = "\033[0m"

def buses(n1, n2):
    output = []
    # Autobús 1 
    output.append(115 * "_")
    output.append((n1 * " ") + "  ________________" + ((100 - n1) * " ") + "|")
    output.append((n1 * " ") + " |                |      " + ((97 - n1) * " ") + "|")
    output.append((n1 * " ") + "|  L_L_L_L_L_L     |__"     + ((97 - n1) * " ") + "|")
    output.append((n1 * " ") + "|[   JHEFER    ]      |)"   + ((96 - n1) * " ") + "|")
    output.append((n1 * " ") + "|_____________________|)"   + ((95 - n1) * " ") + "|")
    output.append((n1 * " ") + "   (O)(0)       (0)(O)   " + ((95 - n1) * " ") + "|")
    output.append(115 * "_")
    
    # Autobús 2 (ABELINO)
    output.append((n2 * " ") + "       _____________" + ((100 - n2) * " ") + "|")
    output.append((n2 * " ") + " _____|         ((  |        " + ((97 - n2) * " ") + "|")
    output.append((n2 * " ") + "|  L_L_L_L_L_L      |________" + ((97 - n2) * " ") + "|")
    output.append((n2 * " ") + "|[  ANGELES   ]         )))) |)" + ((96 - n2) * " ") + "|")
    output.append((n2 * " ") + "|________________________-___|)" + ((95 - n2) * " ") + "|")
    output.append((n2 * " ") + "   (O)(0)       (0)(O)   " + ((95 - n2) * " ") + "|")
    output.append(115 * "_")
    
    return "\n".join(output)

# Bucle opcional para animar los autobuses en la consola
for i in range(0, 70, 2):
    os.system('cls' if os.name == 'nt' else 'clear') # Limpia la pantalla
    print(GREN + buses(i, i // 2) + END)             # El bus 1 avanza más rápido que el bus 2
    time.sleep(0.1)