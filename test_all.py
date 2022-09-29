import subprocess
import glob

if __name__ == '__main__':
    for file in glob.glob('./test/*.txt'):
        print(file)
        subprocess.run(['python3', 'hrd.py', file, 'dfs.txt', 'astar.txt'])