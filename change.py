import os

def rename_files_in_folder(folder_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Sort files to rename them in the right order
    files.sort()

    # Initialize the counter
    counter = 0

    # Rename each file
    for filename in files:
        # Construct the new filename
        new_filename = f"score{counter}.png"  # Assuming the files are all .png format

        # Construct full file paths
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed {filename} to {new_filename}")

        # Increment the counter
        counter += 1

        # If counter exceeds 9, stop renaming
        if counter > 9:
            break

# Example usage
folder_path = "Assets/newFiles"
rename_files_in_folder(folder_path)
