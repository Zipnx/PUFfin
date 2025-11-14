
import sys, json

def load_data(path: str):
    with open(path, 'rb') as f:
        return json.load(f)

def convert(samplelist: list[str]) -> list[str]:
    result = []

    for sample in samplelist:
        sample = bytes.fromhex(sample) 
        # couldve just concatinated the bytes but idc, this is more clear
        lsb = int.from_bytes(sample[0:4], byteorder='big')
        msb = int.from_bytes(sample[4:8], byteorder='big')

        final = (msb << 32) | lsb

        result.append(f'{final:049b}')

    return result

def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <DMPFILE>')
        exit(-1)

    target = sys.argv[1]
    data = load_data(target)

    data['0'] = convert(data['0'])
    data['1'] = convert(data['1'])
    data['2'] = convert(data['2'])

    new_filename = target.split('.')
    new_filename.insert(1, 'converted')
    new_filename = '.'.join(new_filename)
    
    with open(new_filename, 'w') as f:
        json.dump(data, f, indent = 4)
        f.write('\n')
    
    print(f'[+] Saved converted result to "{new_filename}"')

if __name__ == "__main__":
    main()
