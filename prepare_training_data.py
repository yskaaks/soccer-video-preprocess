import os
import shutil
from sklearn.model_selection import train_test_split

# Set your dataset path
dataset_path = 'Data'
# Define the destination path for the new folder structure
os.makedirs('Model Training', exist_ok=True)
destination_path = 'Model Training/Dataset'

def create_directories():
    for split in ['train', 'valid', 'test']:
        for class_dir in os.listdir(dataset_path):
            # Create directory path for each class in train, valid, and test
            dir_path = os.path.join(destination_path, split, class_dir)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

def split_data():
    for class_dir in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_dir)
        images = [os.path.join(class_path, img) for img in os.listdir(class_path) if img.lower().endswith(('png', 'jpg', 'jpeg'))]
        
        # Split the data
        train_val, test = train_test_split(images, test_size=0.1, random_state=42)  # 90-10 split first
        train, valid = train_test_split(train_val, test_size=1/9, random_state=42)  # Split the 90% into 80% train, 10% valid

        # Function to copy files
        def copy_files(files, split):
            for file in files:
                destination_dir = os.path.join(destination_path, split, class_dir)
                shutil.copy(file, destination_dir)

        # Copy files to their respective directories
        copy_files(train, 'train')
        copy_files(valid, 'val')
        copy_files(test, 'test')

if __name__ == "__main__":
    create_directories()  # Create the directory structure
    split_data()  # Split the data and copy files
