import time
import wave
import numpy as np
import scipy as sp
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background') 
plt.rcParams["font.size"] = 18


class TrackedArray():

    def __init__(self, arr, kind="minimal"):
        self.arr = np.copy(arr)
        self.kind = kind
        self.reset()

    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []
        self.full_copies = []

    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        if self.kind == "full":
            self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])

    def __delitem__(self, key):
        self.track(key, "del")
        self.arr.__delitem__(key)

    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()

    def __str__(self):
        return self.arr.__str__()

    def __repr__(self):
        return self.arr.__repr__()




N = 30
FPS = 60
arr = np.round(np.linspace(0, 1000, N), 0)
np.random.seed(0)
np.random.shuffle(arr)

arr = TrackedArray(arr, "full")

np.random.seed(0)

t0 = time.perf_counter()

##############################################
########### DEMO 1 - Insertion Sort ##########
##############################################
sorter = "Insertion"
t0 = time.perf_counter()
i = 1
while (i < len(arr)):
    j = i
    while ((j > 0) and (arr[j-1] > arr[j])):
        temp = arr[j-1]
        arr[j-1] = arr[j]
        arr[j] = temp
        j -= 1

    i += 1
t_ex = time.perf_counter() - t0
############################################
######### DEMO 2 - Quick sort ##############
############################################
# =============================================================================
# sorter = "Quick"


# def quicksort(A, lo, hi):
#     if lo < hi:
#         p = partition(A, lo, hi)
#         quicksort(A, lo, p - 1)
#         quicksort(A, p + 1, hi)


# def partition(A, lo, hi):
#     pivot = A[hi]
#     i = lo
#     for j in range(lo, hi):
#         if A[j] < pivot:
#             temp = A[i]
#             A[i] = A[j]
#             A[j] = temp
#             i += 1
#     temp = A[i]
#     A[i] = A[hi]
#     A[hi] = temp
#     return i


# t0 = time.perf_counter()

# quicksort(arr, 0, len(arr)-1)

# t_ex = time.perf_counter() - t0
#############################################
########## DEMO 3 - Bubble sort ##############
#############################################
# =============================================================================
# sorter = "Bubble"


# def bubbleSort(array):
    
#   for i in range(len(arr)):

#     for j in range(0, len(arr) - i - 1):

#       if arr[j] > arr[j + 1]:

#         temp = arr[j]
#         arr[j] = arr[j+1]
#         arr[j+1] = temp

# bubbleSort(arr)        
# t_ex = time.perf_counter() - t0
#############################################
########## DEMO 4 - Selection sort ##############
#############################################
# =============================================================================
# sorter = "Selection"

# def selectionSort(array, size):
   
#     for step in range(size):
#         min_idx = step

#         for i in range(step + 1, size):
         
#             if arr[i] < arr[min_idx]:
#                 min_idx = i
         
#         (arr[step], arr[min_idx]) = (arr[min_idx], arr[step])
        
# selectionSort(arr, len(arr))
# t_ex = time.perf_counter() - t0
#############################################
########## DEMO 5 - Merge sort ##############
#############################################
# =============================================================================
# sorter = "Heap"

# def heaps(arr, n, i):
#     # Find largest among root and children
#     largest = i
#     l = 2 * i + 1
#     r = 2 * i + 2
    
#     if l < n and arr[i] < arr[l]:
#         largest = l
    
#     if r < n and arr[largest] < arr[r]:
#         largest = r
    
#     # If root is not largest, swap with largest and continue heapifying
#     if largest != i:
#         arr[i], arr[largest] = arr[largest], arr[i]
#         heaps(arr, n, largest)


# def heapSort(arr):
#     n = len(arr)
    
#     # Build max heap
#     for i in range(n//2, -1, -1):
#         heaps(arr, n, i)
    
#     for i in range(n-1, 0, -1):
#         # Swap
#         arr[i], arr[0] = arr[0], arr[i]
    
#         # Heapify root element
#         heaps(arr, i, 0)
  
# heapSort(arr)
# t_ex = time.perf_counter() - t0
# # #######################################################################
# # #######################################################################

        
print(f"---------- {sorter} Sort ----------")
print(f"Array Sorted in {t_ex*1E3:.1f} ms | {len(arr.full_copies):.0f} "
      f"array access operations were performed")



fig, ax = plt.subplots(figsize=(16, 8))
container = ax.bar(np.arange(0, len(arr), 1),
                   arr.full_copies[0], align="edge", width=0.8)
fig.suptitle(f"{sorter} sort")
ax.set(xlabel="Index", ylabel="Value")
ax.set_xlim([0, N])
txt = ax.text(0.01, 0.99, "", ha="left", va="top", transform=ax.transAxes)


def update(frame):
    txt.set_text(f"Accesses = {frame}")
    for rectangle, height in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("teal")

    idx, op = arr.GetActivity(frame)
    if op == "get":
        container.patches[idx].set_color("yellow")
    elif op == "set":
        container.patches[idx].set_color("red")

    fig.savefig(f"frames/{sorter}_frame{frame:05.0f}.png")

    return (txt, *container)

if __name__ == "__main__":

    ani = FuncAnimation(fig, update, frames=range(len(arr.full_copies)),
                        blit=True, interval=1000./FPS, repeat=False)

    plt.show()
