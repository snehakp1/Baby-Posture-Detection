import os
import pandas as pd

def create_image_dataset(root_folder="frames", output_csv="dataset.csv"):
    data = []

    # Loop through movement folders (crawling, sitting, etc.)
    for label in os.listdir(root_folder):
        label_path = os.path.join(root_folder, label)
        print(f"Processing label: {label}")

        if not os.path.isdir(label_path):
            continue
        
        # loop through image files
        for img in os.listdir(label_path):
            if img.lower().endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(label_path, img)

                data.append([img_path.replace("\\", "/"), label])  
                print(f" Added: {img_path} with label: {label}")
    # Create DataFrame
    df = pd.DataFrame(data, columns=["image_path", "label"])

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Dataset saved to {output_csv}")
    print(df.head())

# Run the function
create_image_dataset("frames", "baby_movement_dataset.csv")
