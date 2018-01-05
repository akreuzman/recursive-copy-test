#!/usr/bin/env python3
# -*- coding_UTF-8 -*-

'''
Exploring various methods of copying files recursively from one directory
to another, both locally and uploading to the defiant server.

Goal: to reduce time spent waiting for infant/caregiver files to upload to
defiant.

Result: multiprocessing and concurrent tools are faster when copying files
locally, but make almost no difference when uploading to defiant. The 
slow-down in uploading is caused entirely by the connection to the server
and can't be bypassed by parallel processing. Predictable, but
disappointing.
'''

import os, subprocess, time, shutil, distutils.dir_util
import multiprocessing
import concurrent.futures
from pprint import pprint
import timeit

DIRECTORY = '/Users/snlab/Documents/Projects/huge_files/'
# END_POINT = '/Volumes/Live Data/FromLive/mockinfa/gets_huge_files/'
END_POINT = '/Users/snlab/Documents/Projects/gets_huge_files/'

num_iters = 10 #careful: large numbers of iterations don't play nicely with multiprocessing!

# # Connect to server
# if os.path.exists('/Volumes/Live Data'):
#     print('Already connected to defiant.')
# else:
#     print('Mounting defiant server.')
#     subprocess.call(['open','smb://defiant-nx-74205.marcus.emory.edu/Live%20Data/'])

#     while not os.path.exists('/Volumes/Live Data'):
#         time.sleep(1)
#     print('Connected to defiant.')

# Print list of files
listFiles = os.listdir(DIRECTORY)
print(f'Copying {len(listFiles)} files...')
[print('    ' + fileName) for fileName in listFiles]
print('\n')

# Timing functions
def wrapper(function, *args, **kwargs):
    '''Wraps a function and its arguments into a wrapped object to allow it to be passed to timeit.'''
    def wrapped_func():
        return function(*args, **kwargs)
    return wrapped_func

def avg_timeit(wrappedFunc, numIters):
    '''Calculates average process time using timeit.'''
    totalTime = timeit.timeit(wrappedFunc, number = numIters)
    avgTime = totalTime/numIters
    return avgTime

# Copy function with single filename input
def my_copy(fileName: str):
    shutil.copy(DIRECTORY+fileName, END_POINT)

# Method 1: sequential copy() calls
def seq_copy(listFiles: list):
    [my_copy(fileName) for fileName in listFiles]

print('Method 1:')
wrapped = wrapper(seq_copy, listFiles)
avgTime = avg_timeit(wrapped, num_iters)
print(f'Sequential `copy` calls result in an average time of {avgTime}')


# Method 2: copy_tree()
print('Method 2:')
wrapped = wrapper(distutils.dir_util.copy_tree, DIRECTORY, END_POINT)
avgTime = avg_timeit(wrapped, num_iters)
print(f'Using Python\'s built-in `copy_tree` function results in an average time of {avgTime}')


# Method 3: Multiprocessing
def multiprocess_copy(listFiles: list):
    pool = multiprocessing.Pool()
    pool.map(my_copy, listFiles)

print('Method 3:')
wrapped = wrapper(multiprocess_copy, listFiles)
avgTime = avg_timeit(wrapped, num_iters)
print(f'Using `multiprocessing.Pool` results in an average time of {avgTime}')


# Method 4: Concurrent.futures
def concurrent_copy(listFiles: list):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(my_copy, listFiles)

print('Method 4:')
wrapped = wrapper(concurrent_copy, listFiles)
avgTime = avg_timeit(wrapped, num_iters)
print(f'Using `concurrent.futures` results in an average time of {avgTime}')





