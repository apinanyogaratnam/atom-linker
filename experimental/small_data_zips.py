import gzip
import io


def compress_string(input_string):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='w') as f:
        f.write(input_string.encode())
    return buf.getvalue()


def decompress_string(compressed_data):
    buf = io.BytesIO(compressed_data)
    with gzip.GzipFile(fileobj=buf, mode='r') as f:
        return f.read().decode()


# Example usage
if __name__ == "__main__":
    original_string = "This is an example string to be compressed using gzip. gzip is commonly used for compressing text."

    # Compress the string
    compressed_data = compress_string(original_string)
    print("Original size:", len(original_string))
    print("Compressed size:", len(compressed_data))

    # Decompress the string
    decompressed_string = decompress_string(compressed_data)
    print("Decompressed string:", decompressed_string)
