import shutil
import os
import threading


def split_array(arr, size):
    return [arr[i:i+size] for i in range(0, len(arr), size)]


def move_file(name, src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    dst_path = f"{dst}/{name}"
    shutil.copy(src, dst_path)


def per(x, y):
    s = "{:.2f}".format((x/y)*100)
    s = f"{s}%"
    return s


def workers(files: list, src_path, dst):
    result = []
    threads = []
    def worker(name, src, dst_path):
        r = move_file(name, f"{src}/{name}", dst_path)
        result.append(r)

    for file in files:
        thread = threading.Thread(target=worker, args=(file, src_path, dst))
        threads.append(thread)
        thread.start()
    
    for t in threads:
        t.join()
    
    return result


def main():
    TARGET_DIR = "./html"
    file_list = os.listdir(TARGET_DIR)
    total_files = file_list.__len__()
    print("Total files", total_files)
    file_list = split_array(file_list, 10000)
    count = 1
    fp_count = 1
    for fl in file_list:
        d = workers(fl, TARGET_DIR, f"./split/{count}")
        print(d.__len__(),"Moved")
        break
        count += 1


main()
