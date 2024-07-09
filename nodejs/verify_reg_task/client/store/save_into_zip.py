import zipfile
import os


def split_array(arr, size):
    return [arr[i:i+size] for i in range(0, len(arr), size)]


def move_file_into_zip(file_to_zip, zip_file_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'a') as zipf:
            zipf.write(file_to_zip, os.path.basename(file_to_zip))

        # os.remove(file_to_zip)
        return (file_to_zip, True)
    except Exception as e:
        print(f"An error occurred: {e}")
        return (file_to_zip, False)


def per(x, y):
    s = "{:.2f}".format((x/y)*100)
    s = f"{s}%"
    return s


def main():
    TARGET_DIR = "./html"
    file_list = os.listdir(TARGET_DIR)
    total_files = file_list.__len__()
    print("Total files", total_files)
    file_list = split_array(file_list, 50000)
    count = 1
    fp_count = 1
    for fl in file_list:
        for f in fl:
            move_file_into_zip(f"{TARGET_DIR}/{f}", f"./zip/zip_{count}.zip")
            print(
                f"Stage {count}/{file_list.__len__()}. {per(fp_count,total_files)}")
            fp_count += 1
        # break
        count += 1


main()
