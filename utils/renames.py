import glob
import os

path = "./stim/video/"
fs = glob.glob(os.path.join(path, "*.mp4"))

# for f in fs:
#     new_f = (
#         f.replace("female", "f")
#         .replace("male", "m")
#         .replace(" ", "")
#         .replace("positive", "pos")
#         .replace("neutral", "neu")
#         .replace("negative", "neg")
#         .replace("\\", "/")
#     )
#     # print(f, new_f)
#     os.rename(f, new_f)

for f in fs:
    new_f = f.replace("small_", "").replace("\\", "/")
    # print(f, new_f)
    os.rename(f, new_f)
