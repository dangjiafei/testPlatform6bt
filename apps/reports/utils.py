def get_file_content(filename, size=1024):
    with open(filename) as file:
        while True:
            content = file.read(size)
            if not content:
                break
            yield content
