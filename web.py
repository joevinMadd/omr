import omr, utilis
import time


start_time = time.time()

csv_path = utilis.select_csv_file()
images = utilis.choose_folder()

omr.omr(csv_path,images)

# Calculate elapsed time
elapsed_time = time.time() - start_time

# Convert the time to hours, minutes, and seconds
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)

print("Process finished --- %d hours, %d minutes, and %d seconds ---" % (hours, minutes, seconds))