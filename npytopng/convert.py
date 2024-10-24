import cv2
import numpy as np
import os
from tqdm import tqdm  # For progress bar

def extract_and_save_arrays(input_npy_path, output_folder, max_samples=None):

    # Load the NPY file
    print(f"Loading NPY file: {input_npy_path}")
    # Fix: Remove quotes from input_npy_path
    data = np.load(input_npy_path)  # Changed from "input_npy_path" to input_npy_path
    print(f"Loaded array shape: {data.shape}")
    print(f"Array data type: {data.dtype}")
    
    # Create output folders if they don't exist
    png_folder = os.path.join(output_folder, 'png')
    npy_folder = os.path.join(output_folder, 'npy')
    os.makedirs(png_folder, exist_ok=True)
    os.makedirs(npy_folder, exist_ok=True)
    
    # Determine number of samples to process
    n_samples = len(data) if max_samples is None else min(len(data), max_samples)
    print(f"Processing {n_samples} samples...")
    
    # Process each array
    for i in tqdm(range(n_samples)):
        # Get single array
        if len(data.shape) == 2 and data.shape[1] == 784:  # MNIST-like data
            # Reshape from (784,) to (28, 28)
            single_array = data[i].reshape(28, 28)
            
            # Scale to 0-255 if needed
            if single_array.dtype != np.uint8:
                single_array = ((single_array - single_array.min()) * 255 / 
                              (single_array.max() - single_array.min())).astype(np.uint8)
            
            # Convert to RGB for visualization
            image = cv2.cvtColor(single_array, cv2.COLOR_GRAY2BGR)
            
        elif len(data.shape) == 4:  # Batch of RGB/BGR images
            single_array = data[i]
            image = single_array
            
        elif len(data.shape) == 3:  # Single RGB image or batch of grayscale
            single_array = data[i]
            if len(single_array.shape) == 2:  # Grayscale
                image = cv2.cvtColor(single_array, cv2.COLOR_GRAY2BGR)
            else:  # RGB/BGR
                image = single_array
                
        else:
            raise ValueError(f"Unsupported array shape: {data.shape}")
        
        # Generate filenames
        png_filename = os.path.join(png_folder, f'image_{i:06d}.png')
        npy_filename = os.path.join(npy_folder, f'image_{i:06d}.npy')
        
        # Save as PNG
        cv2.imwrite(png_filename, image)
        
        # Save as NPY
        np.save(npy_filename, single_array)
    
    print(f"\nProcessing complete!")
    print(f"PNG files saved in: {png_folder}")
    print(f"NPY files saved in: {npy_folder}")
    return png_folder, npy_folder

def main():
    # Example usage
    input_npy_path = "full_numpy_bitmap_airplane.npy"  # Your input NPY file
    output_folder = "output"  # Output folder name
    max_samples = None  # Set to a number if you want to limit the samples
    
    try:
        # Add file existence check
        if not os.path.exists(input_npy_path):
            print(f"Error: Input file '{input_npy_path}' not found.")
            return
            
        png_folder, npy_folder = extract_and_save_arrays(
            input_npy_path, 
            output_folder,
            max_samples
        )
        
        # Print some statistics
        n_png_files = len(os.listdir(png_folder))
        n_npy_files = len(os.listdir(npy_folder))
        print(f"\nStatistics:")
        print(f"Number of PNG files created: {n_png_files}")
        print(f"Number of NPY files created: {n_npy_files}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()