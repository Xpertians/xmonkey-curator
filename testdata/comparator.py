import ssdeep

# Load ssdeep hashes from the provided file
file_path = 'hashes.txt'
with open(file_path, 'r') as f:
    hashes = [line.strip() for line in f if line.strip()]

# Calculate similarity scores between each pair of hashes
similarity_scores = []
for i in range(len(hashes)):
    for j in range(i + 1, len(hashes)):
        score = ssdeep.compare(hashes[i], hashes[j])
        similarity_scores.append(((i, j), score))

for pair, score in similarity_scores:
    print(f"Hash {pair[0]} vs Hash {pair[1]}: {score}% similarity")

