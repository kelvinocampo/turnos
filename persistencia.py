def guardar_info(data, filename):
    with open(filename, 'w') as f:
        for entry in data:
            f.write(f"{entry}\n")