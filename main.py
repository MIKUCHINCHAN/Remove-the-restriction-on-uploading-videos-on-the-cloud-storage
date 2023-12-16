import os
import time
import re
import subprocess
from datetime import datetime

# 遍历目录内的所有视频文件并存到指定目录
path = '''C:\\Users\\HATSUNEMIKU\\Downloads'''  # 要遍历的目录
ALL_FILES=[]
VEDIO_FORMATS=['.mp4','.flv','.f4v','.webm','.m4v','.mov','.3gp','.3g2','.rm','.rmvb','.wmv','.avi','.asf','.mpg','.mpeg','.mpe','.ts','.div','.mkv']
for root, dirs, names in os.walk(path):
    for name in names:
        ext = os.path.splitext(name)[1]  # 获取后缀名
        if ext in VEDIO_FORMATS:
            fromdir = os.path.join(root, name)  # mp4文件原始地址
            ALL_FILES.append(fromdir)

for  _ in ALL_FILES:

    print("⬛⬛⬛⬛⬛⬛正在处理：",_)
    # 获取视频信息
    res =  subprocess.Popen(f'''ffprobe -i "{_}"''', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    content=str(res.stdout.read(),'utf-8')
    res.stdout.close()  # 关闭
    duration=re.search("\d\d:\d\d:\d\d", content, flags=0).group()  #视频持续时间

    print("⬛⬛⬛⬛⬛⬛duration：",duration)

    hour = duration[0:2]
    minute = duration[3:5]
    second = duration[6:8]



    if second =='00':
        if minute != '00':
            new_duration =hour+":"+str(int(minute)-1).rjust(2, '0')+":"+minute
        else:
            new_duration = str(int(hour) - 1).rjust(2, '0') + ":" +"59" + ":" +"00"
    else:

        new_duration = hour + ":" + minute + ":" + str(int(second) - 1).rjust(2, '0')

    print("⬛⬛⬛⬛⬛⬛new_duration：",new_duration)

    # 剪辑1秒
    res = subprocess.Popen(f'''ffmpeg -ss 00:00:00 -to {new_duration} -i "{_}" -c:v copy "{_.split(_.split('.')[-1])[0]+"_output."+_.split('.')[-1]}"''', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    print(f'''⬛⬛⬛⬛⬛⬛code：ffmpeg -ss 00:00:00 -to {new_duration} -i '{_}' -c:v copy "{_.split(_.split('.')[-1])[0]+"_output."+_.split('.')[-1]}''')

    content = str(res.stdout.read(), 'utf-8')
    res.stdout.close()  # 关闭

    print("▶▶▶▶▶▶处理完成：",_)
