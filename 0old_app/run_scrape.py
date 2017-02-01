import sys

import time

import engine
from tools.general_tools import utc_now

pageids_pol = [
    # Open VLD
    '53668151866',  # VLD
    '149158155084',  # Gwendolyn Rutten
    '228307843991539',  # Alexander De Croo
    '62130106444',  # Philippe De Backer
    '1516688831944301',  # Bart Tommelein
    '100947845480',  # Sven Gatz

    # NVA
    '334361224413',  # NVA
    '649429725077632',  # Geert Bourgois
    '483497581789280',  # Theo Franken
    '60317812912',  # Jan Janbon
    '197625717055207',  # Philippe Muyters
    '133467219125',  # Ben Weyts
    '434653689973297',  # Jan Peumans
    '543319679114946',  # Matthias Diependaele
    '260207497491940',  # Annick De Ridder
    '983442595060481',  # Steven Vandeput
    '571227032971640',  # Elke Sleurs
    # '290425771053430',  # Siegfried Bracke
    '453932394796444',  # Zuhal Demir

    # SPA
    '57253967150',  # SPA
    '264131406977201',  # John Crombez
    '208965559294791',  # Carolinne Gennez
    '206193139504506',  # Kathleen Van Bempt
    '148221008918941',  # Pascal Smet
    '107667452691841',  # Renaat Landuyt

    # CD&V
    '52997544531',  # CD&V
    '311935738907850',  # Wouter Beke
    '192181027566488',  # Kris Peeters
    '294055357407926',  # Koen Geens
    '1417661025148910',  # Sabine de Bethune

    # Groen
    '84920854319',  # Groen
    '345099982367937',  # Kristof Calvo
    '37339765706',  # Bart Staes

    # Vlaams Belang
    '56605856504',  # Vlaams Belang
    '584806884924010',  # Tom Van Grieken
    '103536906359022',  # Filip De Winter
    '240191162725859',  # Anke Van Dermeersch

    # PVDA
    '54970503767',  # PVDA Belgie
    '236485149843971',  # Peter Mertens
    '305365056290036',  # Raoul Hedebouw

    # Nederland
    '202064936858448',  # Geert Wilders
]
pageids_news = [
    # Kranten
    '231742536958',  # De Morgen
    '270994524621',  # VRT De Redactie
    '223630074319030',  # VTM Nieuws
    '345644812211706',  # Het Laatste Nieuws

    '7133374462',  # De Standaard
    '37823307325',  # Het Nieuwsblad
    '10461114902',  # De Tijd
    '134679853231866',  # Het Pallieterke
    '443387969094801',  # Newsmonkey
]
pageids_test = ['983442595060481']
resume = False
ENG = engine.Engine(since=(2017, 1, 10), until=(2018, 1, 1))

list_nr = int(raw_input('Enter (1:politics, 2:news, id): '))
if list_nr == 0:
    page_ids = pageids_pol + pageids_news
    bulkdays = 2
    lst = 'ALL'
elif list_nr == 1:
    page_ids = pageids_pol
    bulkdays = 3
    lst = 'POLITICS'
elif list_nr == 2:
    page_ids = pageids_news
    bulkdays = 1
    lst = 'NEWS'
elif list_nr > 1000:
    page_ids = ['{}'.format(list_nr)]
    bulkdays = int(raw_input('Enter bulkdays: '))
    lst = list_nr
else:
    page_ids = ['37823307325']
    bulkdays = 2
    lst = 'TEST'
i = 0
print '\n{} Start scraping list: {}. Attempt: {}\n'.format(utc_now(), lst, i)
while i < 10:
    try:
        result = ENG.run_scraping(pageidlist=page_ids, resume=resume, bulkdays=bulkdays)
        if result:
            print '{} End scraping list {}'.format(utc_now(), lst)
            break
    except:
        e = sys.exc_info()[0]
        print e
        i += 1
        time.sleep(600)

# ENG.run_scraping(pageidlist=['446368145415026'], resume=False, bulkdays=30)
