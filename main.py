import requests, os
import tkinter as tk

client = None
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

while client == None:
    response = input('Is this for a client? (y/n)').lower()

    if response == 'y':
        client = True
        GUI = None
        
        while GUI == None:
            response = input('Would you like a gui? (y/n)').lower()

            if response == 'y':
                GUI = True

            elif response == 'n':
                GUI = False

    elif response == 'n':
        client = False
        GUI = False

if GUI:
    root = tk.Tk()

def forge_install():
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
        
to_delete = []
def mod_install():
    if to_delete != []:
        for mod in to_delete:
            #if globals()[f'{mod}_delete_var'].get():
                #os.remove(f'mods/{mod}.jar')
                #print(f'Deleted {mod}.jar')
            pass

    if GUI:
        root.destroy()

    for mod in mods:
        if (mod.startswith('--server--') and client == False) or (mod.startswith('--client--') and client == True) or (mod.startswith('--server--') == mod.startswith('--client--')):
            mod = mod.replace('--server--', '').replace('--client--', '')
            names = mod.split('/')
            for entry in names:
                if '.jar' in entry:
                    name = entry
                    break
                
            if name not in installed:
                data = requests.get(mod).content

                with open(f'mods/{name}', 'wb') as file:
                    file.write(data)

                print(f'{name} installed')

            else:
                print(f'{name} detected')

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def generate_canvas(region):
    globals()[f'{region}_canvas'] = tk.Canvas(root)
    globals()[f'{region}_frame'] = tk.Frame(globals()[f'{region}_canvas'])
    globals()[f'{region}_vsb'] = tk.Scrollbar(root, orient=tk.VERTICAL, command=globals()[f'{region}_canvas'].yview)
    globals()[f'{region}_canvas'].configure(yscrollcommand=globals()[f'{region}_vsb'].set)

    placement = {
        'all':(1,0),
        'detected':(1,2),
        'install':(1,4),
        'delete':(1,6)
    }

    globals()[f'{region}_vsb'].grid(row=placement[region][0], column=placement[region][1]+1, rowspan=len(mods))
    globals()[f'{region}_canvas'].grid(row=placement[region][0], column=placement[region][1], rowspan=len(mods))
    globals()[f'{region}_canvas'].create_window((4,4), window=globals()[f'{region}_frame'], anchor="nw")

    globals()[f'{region}_frame'].bind("<Configure>", lambda event, canvas=globals()[f'{region}_canvas']: onFrameConfigure(canvas))

forge_install()

if GUI:
    labels = ('All', 'Detected', 'To Install', 'To Delete(NonFunctional)')
    for column, label in enumerate(labels):
        globals()[f'{label}_label'] = tk.Label(root, text=label).grid(row=0, column=column*2, columnspan=2)

    generate_canvas('all')

    rows_all = 1
    for mod in mods:
        if mod.startswith('--server--'):
            mods.remove(mod)

        else:
            mods[mods.index(mod)] = mod.replace('--client--', '')

    link_names = []
    for mod in sorted(mods):
        names = mod.split('/')
        for entry in names:
            if '.jar' in entry:
                name = entry
                link_names.append(name)
                break

        globals()[f'{name}_all_label'] = tk.Label(all_frame, text=name, justify=tk.LEFT).grid(row=rows_all, column=0, sticky=tk.W)
        rows_all += 1


    generate_canvas('detected')

    for row, mod in enumerate(installed):
        globals()[f'{name}_detected_label'] = tk.Label(detected_frame, text=mod, justify=tk.LEFT).grid(row=row, column=0, sticky=tk.W)


    generate_canvas('install')
    
    install_rows = 0
    for mod in link_names:
        if mod not in installed:
            globals()[f'{name}_install_label'] = tk.Label(install_frame, text=mod, justify=tk.LEFT).grid(row=install_rows, column=0, sticky=tk.W)
            install_rows += 1


    generate_canvas('delete')

    delete_rows = 0
    for mod in installed:
        if mod not in link_names and '.jar' in mod:
            to_delete.append(mod.replace('.jar',''))
            globals()[f"{name.replace('.jar','')}_delete_var"] = tk.BooleanVar
            globals()[f'{name}_delete_button'] = tk.Checkbutton(delete_frame, variable=globals()[f"{name.replace('.jar','')}_delete_var"]).grid(row=delete_rows, column=0)
            globals()[f'{name}_delete_label'] = tk.Label(delete_frame, text=mod, justify=tk.LEFT).grid(row=delete_rows, column=1, sticky=tk.W)
            delete_rows += 1

    start_button = tk.Button(root, text='START', command=mod_install).grid(row = len(mods)+5, column = 0)

    root.mainloop()

else:
    mod_install()