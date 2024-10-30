from PIL import Image
import numpy as np


# Function to calculate similarity between two black-and-white images
def calculate_similarity(image_path1, image_path2):
    # Load the images and convert them to black and white (1-bit pixels)
    image1 = Image.open(image_path1).convert("1")
    image2 = Image.open(image_path2).convert("1")

    # Resize image1 to match the size of image2 if they differ
    image1 = image1.resize(image2.size)

    # Convert the images to numpy arrays for easier processing
    image1_np = np.array(image1)
    image2_np = np.array(image2)

    # Calculate total number of pixels and count matching pixels
    total_pixels = image1_np.size
    matching_pixels = np.sum(image1_np == image2_np)

    # Helper function to find paths of connected pixels in an image
    def find_paths(image_np):
        visited = np.zeros(image_np.shape, dtype=bool)  # Track visited pixels
        paths = []  # Store all discovered paths

        # Depth-first search function to explore connected pixels
        def dfs(x, y, path):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if visited[cx, cy]:
                    continue
                visited[cx, cy] = True  # Mark current pixel as visited
                path.append((cx, cy))  # Add pixel to the current path

                # Check neighbors in four directions
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < image_np.shape[0] and 0 <= ny < image_np.shape[1]:
                        if image_np[nx, ny] == 1 and not visited[nx, ny]:
                            stack.append((nx, ny))

        # Iterate over each pixel in the image
        for i in range(image_np.shape[0]):
            for j in range(image_np.shape[1]):
                if image_np[i, j] == 1 and not visited[i, j]:
                    path = []  # Initialize a new path
                    dfs(i, j, path)  # Perform DFS to find connected pixels
                    paths.append(path)  # Add the path to the list

        return paths

    # Find connected paths in both images
    paths_image1 = find_paths(image1_np)
    paths_image2 = find_paths(image2_np)

    # Calculate the difference in the number of paths
    differing_paths = abs(len(paths_image1) - len(paths_image2))

    # Calculate path similarity score based on path count
    path_similarity_score = 1 - (
        differing_paths / max(len(paths_image1), len(paths_image2), 1)
    )

    # Convert pixel similarity score to a percentage
    pixel_similarity_percentage = (matching_pixels / total_pixels) * 100
    # Convert path similarity score to a percentage
    path_similarity_percentage = path_similarity_score * 100
    # Calculate overall similarity by averaging pixel and path similarity percentages
    overall_similarity_score = (pixel_similarity_percentage * 0.5) + (
        path_similarity_percentage * 0.5
    )

    # Return all calculated metrics
    return {
        "total_pixels": total_pixels,
        "matching_pixels": matching_pixels,
        "pixel_similarity_percentage": pixel_similarity_percentage,
        "path_similarity_percentage": path_similarity_percentage,
        "overall_similarity_score": overall_similarity_score,
    }


# Example usage
result = calculate_similarity("blocked_region.png", "test2.png")
print(f"Total Pixels: {result['total_pixels']}")
print(f"Matching Pixels: {result['matching_pixels']}")
print(f"Pixel Similarity Percentage: {result['pixel_similarity_percentage']:.2f}%")
print(f"Path Similarity Percentage: {result['path_similarity_percentage']:.2f}%")
print(f"Overall Similarity Score: {result['overall_similarity_score']:.2f}%")


# Code only for Pixel Count and not including the DFS

# from PIL import Image
# import numpy as np

# # Function to calculate pixel similarity between two black-and-white images
# def calculate_similarity(image_path1, image_path2):
#     # Load the images and convert them to black and white (1-bit pixels)
#     image1 = Image.open(image_path1).convert("1")
#     image2 = Image.open(image_path2).convert("1")

#     # Resize image1 to match the size of image2 if they differ
#     image1 = image1.resize(image2.size)

#     # Convert the images to numpy arrays for easier processing
#     image1_np = np.array(image1)
#     image2_np = np.array(image2)

#     # Calculate total number of pixels and count matching pixels
#     total_pixels = image1_np.size
#     matching_pixels = np.sum(image1_np == image2_np)

#     # Calculate pixel similarity percentage
#     pixel_similarity_percentage = (matching_pixels / total_pixels) * 100

#     # Return the calculated metrics
#     return {
#         "total_pixels": total_pixels,
#         "matching_pixels": matching_pixels,
#         "pixel_similarity_percentage": pixel_similarity_percentage,
#     }

# # Example usage
# result = calculate_similarity("blocked_region.png", "test2.png")
# print(f"Total Pixels: {result['total_pixels']}")
# print(f"Matching Pixels: {result['matching_pixels']}")
# print(f"Pixel Similarity Percentage: {result['pixel_similarity_percentage']:.2f}%")
