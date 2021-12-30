import numpy as np
from dfs import neighbor, dfs, path_length


def edge_detect(skeleton_pad):
    ## edge detect
    (rows,cols) = np.nonzero(skeleton_pad)
    edges = []
    for (r,c) in zip(rows,cols):
        neighs = neighbor(skeleton_pad, r, c)
        neighs_nonzero = (neighs.ravel() != 0)
        nearby_score = np.sum(neighs_nonzero)
        if nearby_score == 1:
            skeleton_pad[r,c] = 0
        elif nearby_score == 2:
            edges.append((r,c))
        else:
            pass
    return edges


def get_info(skeleton_pad):
    (height, width) = skeleton_pad.shape
    ## edge detect
    edges = edge_detect(skeleton_pad)
    info = []
    if len(edges):
        for (r,c) in edges:
            visited_init = np.zeros((height,width))
            hierarchy_init = np.zeros((height,width))
            end_save, hierarchy = dfs(skeleton_pad, (r,c), visited=visited_init, hierarchy=hierarchy_init, h=1, p_save=[]) # find ends of paths from (r,c)
            pl_save = []
            for end in end_save:
                path_len = path_length(hierarchy, end)
                if len(edges)%2==0:           # edge pair exist?
                    if end not in edges:      # if exist and end is not in edge group (e.g loop point)
                        pl_save.append(0)
                        continue
                pl_save.append(path_len)                # if edge pair not exist take loop point as edge
            pl_save = np.array(pl_save) 
            info.append([(r,c), end_save[np.argmax(pl_save)], np.max(pl_save)])   # take longest path from (r,c)
    return info


def longest_path(info):
    pls = np.zeros(len(info))
    for idx in range(len(info)):
        pls[idx] = info[idx][2]
    max_idx = np.argmax(pls)       # select maximum length path among all
    (rM,cM) = info[max_idx][0]
    endM = info[max_idx][1]
    lenM = info[max_idx][2]

    ## pad coordinate adjustment
    rM = rM-1
    cM = cM-1
    endrM = endM[0]-1
    endcM = endM[1]-1

    start = (rM, cM)
    end = (endrM, endcM)
    return start, end, lenM