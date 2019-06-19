import os
import exifread

def send_to_trashbin(filename, cur_path):
    
    
    trash_path = os.path.join(r'\\HUSSEY_NAS\Hussey Share\trashbin', filename)
    try:
        print(f'Moved {cur_path} to {trash_path}')
        os.rename(cur_path, trash_path)
    except FileExistsError:
        print(f'{cur_path} is already in trashbin, just deleting it.')
        os.remove(cur_path)


no_date, ss_cnt, movie_cnt, db_cnt = 0, 0, 0, 0

for root, dirs, files in os.walk(r'\\HUSSEY_NAS\Hussey Share\Pictures'):
    for name in files:
        path = os.path.join(root, name)
        with open(path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            try:
                print(f'{name} take at {tags["EXIF DateTimeOriginal"]}')
            except KeyError:
                no_date += 1
                print(f'*******{name} has no DateTimeOriginal')
        name = name.upper()

        if '.AAE' in name :
            ss_cnt += 1
            send_to_trashbin(name, path)
        elif '.PNG' in name and 'Purchased' not in path:
            ss_cnt += 1
            send_to_trashbin(name, path)
        elif '.DB' in name or 'THUMBS' in name:
            db_cnt += 1
            send_to_trashbin(name, path)
        elif '.MOV' in name or '.MP4' in name or '.WMV' in name or '.MPG' in name:
            items = path.split('\\')
            print(items)
            dst_path = os.path.join(r'\\HUSSEY_NAS\Hussey Share\Videos', items[5], name)
            dst_dir = os.path.join(r'\\HUSSEY_NAS\Hussey Share\Videos', items[5])
            print(f'>>>> Moving {path} to \n\t   {dst_path}')
            if not os.path.isdir(dst_dir):  #create the dir if it doesn't already exist
                os.mkdir(dst_dir)
            try:
                os.rename(path, dst_path)   #rename effectively moves it
            except FileExistsError:         #crudely handle the case where we've copied this exact video once before
                try:
                    os.rename(path, dst_path + '_2')
                except FileExistsError:
                    os.rename()
            movie_cnt += 1


print(f'Total movies found {movie_cnt}\nTotal thumbnails found {db_cnt}\nTotal screenshots found {ss_cnt}')
print(f'{no_date} files had no date taken')
