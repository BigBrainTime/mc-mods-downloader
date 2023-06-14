with open('mods.txt', 'r') as file:
    data = file.readlines()

data.sort()

forge_files = []
for mod in data:
    if mod.startswith('--forge--'):
        forge_files.append(mod)
        data.remove(mod)

for mod in reversed(forge_files):
    data.insert(0, mod)

for line in data:
    print(line)