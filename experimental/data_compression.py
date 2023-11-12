import lzma

def compress_string(input_string):
    compressed_data = lzma.compress(input_string.encode())
    return compressed_data


def decompress_string(compressed_data):
    decompressed_data = lzma.decompress(compressed_data)
    return decompressed_data.decode()


# Example usage
if __name__ == "__main__":
    original_string = "This is an example string to be compressed using LZMA. LZMA provides a high compression ratio!" * 100000000000

    # Compress the string
    compressed_data = compress_string(original_string)
    print("Original size:", len(original_string))
    print("Compressed size:", len(compressed_data))

    # Decompress the string
    decompressed_string = decompress_string(compressed_data)
    # print("Decompressed string:", decompressed_string)

