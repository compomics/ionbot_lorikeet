import sys
import os

base_path = ''
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.join(os.getcwd())

# Read unimod modifications file
def read_deltas(unimod_file):
    deltas = {}
    with open(unimod_file)  as f:
        for row in f:
            l = row.rstrip().split(',')
            unimod = l[0].split('[')[1].split(']')[0]
            deltas[unimod] = float(l[1])
    return deltas

def main():
    unimod_file = os.path.join(base_path, 'unimodptms.txt')
    mgf_file_dir = sys.argv[1]

    deltas = read_deltas(unimod_file)

    # varmods_list = []
    # if modifications != "N":
    #     varmods_list = get_varmods(sequence, modifications, deltas)

if __name__ == "__main__":
    main()