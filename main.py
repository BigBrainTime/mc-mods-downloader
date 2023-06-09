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

if 'forgeinstaller.jar' not in os.listdir() and mods[0].startswith('--forge--'):
    data = requests.get(mods[0].replace('--forge--', '')).content
    mods.pop(0)

    with open(f'forgeinstaller.jar', 'wb') as file:
        file.write(data)

    print('forge installed')

else:
    if mods[0].startswith('--forge--'):
        mods.pop(0)
    print('forge detected')

client = input('Is this for a client?')

for mod in mods:
    if (mod.startswith('--server--') and client == False) or (mod.startswith('--client--') and client == True) or (mod.startswith('--server--') == mod.startswith('--client--')):
        mod = mod.replace('--server--', '').replace('--client--', '')
        name = mod.split('/')[6]
        if name not in installed:
            data = requests.get(mod).content

            with open(f'mods/{name}', 'wb') as file:
                file.write(data)

            print(f'{name} installed')

        else:
            print(f'{name} detected')