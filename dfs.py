import numpy as np


def neighbor(image, r, c):
    (col_neigh,row_neigh) = np.meshgrid(np.array([c-1,c,c+1]), np.array([r-1,r,r+1]))
    col_neigh = col_neigh.astype(np.uint16)
    row_neigh = row_neigh.astype(np.uint16)
    return image[row_neigh,col_neigh]


def dfs(image, p, visited, hierarchy, h, p_save):
    visited[p[0],p[1]] = 1
    hierarchy[p[0],p[1]] = h
    (height,width) = image.shape
    if not (p[0]==0 or p[0]==height or p[1]==0 or p[1]==width): # not border
        neighs  = neighbor(image, p[0], p[1])
        pix_nonzero = np.argwhere(neighs!=0) - 1 # point existence
        
        endcheck = 1
        for p_n in pix_nonzero:
            p_u = p+p_n
            endcheck *= visited[p_u[0],p_u[1]]

        if endcheck==1: # if all existing point are visited, the point p is the end
            p_save.append(p)
        else:
            for idx, p_n in enumerate(pix_nonzero):
                p_u = p+p_n
                if not visited[p_u[0], p_u[1]]:
                    if len(pix_nonzero)>3: # the line is splitted, so the hierarchy is renewed
                        dfs(image, (p_u[0], p_u[1]), visited, hierarchy, h*10+idx, p_save)
                    else:
                        dfs(image, (p_u[0], p_u[1]), visited, hierarchy, h, p_save)
                else:
                    pass
    else:
        p_save.append(p)
    return p_save, hierarchy


def path_length(hierarchy, end):
    h_code = int(hierarchy[end[0],end[1]])
    h_unique, h_counts = np.unique(hierarchy, return_counts=True)
    h_dict = dict(zip(h_unique, h_counts))
    h_sum = 0
    for c in range(len(str(h_code)),0,-1):
        h_sum += h_dict[int(h_code/pow(10,c-1))]
    # ex) If h_code = 102, h_sum = n(1) + n(10) + n(102)
    return h_sum
