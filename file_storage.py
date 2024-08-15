import pickle


def save_data(data_dict, filename="storage.bin"):
    with open(filename, "wb") as f:
        pickle.dump(data_dict, f)


def load_data(filename="storage.bin"):
    with open(filename, "rb") as f:
        return pickle.load(f)
