import requests, os

debug = False

if debug:
    with open('mods.txt', 'r') as file:
        mods = file.read()

else:
    mods = requests.get('https://github.com/BigBrainTime/mc-mods-downloader/raw/main/mods.txt').content
    mods = mods.decode()

mods = mods.split('\n')

if 'mods' not in os.listdir():
    os.mkdir('mods')
    installed = []
else:
    installed = os.listdir('mods')

if 'forgeinstaller.jar' not in os.listdir():
    data = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.1.0/forge-1.19.4-45.1.0-installer.jar').content

    with open(f'forgeinstaller.jar', 'wb') as file:
        file.write(data)

    print('forge installed')

else:
    print('forge detected')

for mod in mods:
    name = mod.split('/')[6]
    if name not in installed:
        data = requests.get(mod).content

        with open(f'mods/{name}', 'wb') as file:
            file.write(data)

        print(f'{name} installed')

    else:
        print(f'{name} detected')