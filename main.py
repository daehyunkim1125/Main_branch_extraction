import os, cv2
import numpy as np

from skimage.morphology import skeletonize
from longest_path_ext import get_info, longest_path


path = 'data_ex/gt_ex/'
files = os.listdir(path)

starts = []
ends = []
for file in files:
    file_path = os.path.join(path, file)
    image = cv2.imread(file_path)
    skel = skeletonize((image>0).astype(np.uint8), method='lee')
    skel_pad = np.pad(skel, ((1,1),(1,1)), 'constant', constant_values=0)

    info = get_info(skel_pad)
    start, end, lenM = longest_path(info)

    starts.append(start)
    ends.append(end)
