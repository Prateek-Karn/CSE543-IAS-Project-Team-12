from PIL import Image
import numpy as np


def calculate_similarity(image_path1, image_path2):
    image1 = Image.open(image_path1).convert("1")
    image2 = Image.open(image_path2).convert("1")
    image1 = image1.resize(image2.size)

    image1_np = np.array(image1)
    image2_np = np.array(image2)

    total_pixels = image1_np.size
    matching_pixels = np.sum(image1_np == image2_np)

    def find_paths(image_np):
        visited = np.zeros(image_np.shape, dtype=bool)
        paths = []

        def dfs(x, y, path):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if visited[cx, cy]:
                    continue
                visited[cx, cy] = True
                path.append((cx, cy))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < image_np.shape[0] and 0 <= ny < image_np.shape[1]:
                        if image_np[nx, ny] == 1 and not visited[nx, ny]:
                            stack.append((nx, ny))

        for i in range(image_np.shape[0]):
            for j in range(image_np.shape[1]):
                if image_np[i, j] == 1 and not visited[i, j]:
                    path = []
                    dfs(i, j, path)
                    paths.append(path)

        return paths

    paths_image1 = find_paths(image1_np)
    paths_image2 = find_paths(image2_np)

    differing_paths = abs(len(paths_image1) - len(paths_image2))

    path_similarity_score = 1 - (
        differing_paths / max(len(paths_image1), len(paths_image2), 1)
    )

    # Convert scores to percentages
    pixel_similarity_percentage = (matching_pixels / total_pixels) * 100
    path_similarity_percentage = path_similarity_score * 100
    overall_similarity_score = (pixel_similarity_percentage * 0.5) + (
        path_similarity_percentage * 0.5
    )

    return {
        "total_pixels": total_pixels,
        "matching_pixels": matching_pixels,
        "pixel_similarity_percentage": pixel_similarity_percentage,
        "path_similarity_percentage": path_similarity_percentage,
        "overall_similarity_score": overall_similarity_score,
    }


# Example usage
result = calculate_similarity("blocked_region.png", "test.png")
print(f"Total Pixels: {result['total_pixels']}")
print(f"Matching Pixels: {result['matching_pixels']}")
print(f"Pixel Similarity Percentage: {result['pixel_similarity_percentage']:.2f}%")
print(f"Path Similarity Percentage: {result['path_similarity_percentage']:.2f}%")
print(f"Overall Similarity Score: {result['overall_similarity_score']:.2f}%")
