import subprocess
import os, glob

path = "C:\\Users\\micha\\Documents\\cyberball\\cyberball\\stim\\video"
videos = glob.glob(os.path.join(path, "*.mp4"))

ffmpeg_exe = "C:\\Users\\micha\\Downloads\\ffmpeg-4.4-essentials_build\\bin\\ffmpeg.exe"

# batch resize
# for v in videos:
#     output = os.path.join(path, "small_" + os.path.basename(v))
#     print(output)
#     subprocess.run([ffmpeg_exe, "-i", v, "-vf", "scale=400:300", output])

# batch reverse
for v in videos:
    output = os.path.join(path, "reversed_" + os.path.basename(v))
    print(output)
    subprocess.run([ffmpeg_exe, "-i", v, "-vf", "reverse", output])
