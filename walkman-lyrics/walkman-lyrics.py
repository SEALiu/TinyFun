import codecs
import os
import re
import time
import progressbar

if __name__ == '__main__':
    path = './data'

    # 用于显示处理进度 
    file_num = len(os.listdir(path))
    file_index = 0
    pb = progressbar.ProgressBar()
    pb.start(file_num)

    for file in os.listdir(path):
        if file[-3:] != 'lrc':
            continue
        print('Processing >>>> ' + file)

        lyrics = codecs.open(path + file, 'r+', 'utf-8-sig', errors='ignore')
        rows = lyrics.readlines()

        lyrics.seek(0)
        for row in rows:
            pattern1 = re.compile(r'(\[\d{2}:\d{2}.\d{3}\])([\w|\W]*?)[\n]')
            m1 = pattern1.match(row)

            if m1:
                new_row = m1.group(1)[:-2] + ']' + m1.group(2) + '\n'
                lyrics.write(new_row)
            else:
                lyrics.write(row)

        lyrics.close()
        
        file_index += 1
        pb.update(file_index)
    
    pb.finish()