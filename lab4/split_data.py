import os
import shutil
from sklearn.model_selection import train_test_split
import zipfile

base_dir = "archive/flowers"

if not os.path.exists(base_dir):
    print(f"Папка '{base_dir}' не найдена. Разархивируем 'archive.zip'...")
    with zipfile.ZipFile("archive.zip", "r") as zip_ref:
        zip_ref.extractall("archive")
    print("Разархивация завершена.")

train_ratio = 0.8

train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

categories = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

for category in categories:
    category_path = os.path.join(base_dir, category)
    if category in ["train", "val"]:
        continue

    images = [img for img in os.listdir(category_path) if img.endswith(".jpg")]
    if len(images) == 0:
        continue

    train_images, val_images = train_test_split(images, train_size=train_ratio, random_state=42)

    train_category_dir = os.path.join(train_dir, category)
    val_category_dir = os.path.join(val_dir, category)
    os.makedirs(train_category_dir, exist_ok=True)
    os.makedirs(val_category_dir, exist_ok=True)

    for img in train_images:
        shutil.move(os.path.join(category_path, img), os.path.join(train_category_dir, img))
    for img in val_images:
        shutil.move(os.path.join(category_path, img), os.path.join(val_category_dir, img))

    print(f"Категория '{category}': {len(train_images)} train, {len(val_images)} val")

for category in categories:
    category_path = os.path.join(base_dir, category)
    if not os.listdir(category_path):
        print(f"Папка '{category}' пустая - удаление.")
        os.rmdir(category_path)
