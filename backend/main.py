from src.utils import loaders

def main():
    data = loaders.load_message_data('data')
    print(data)

if __name__ == "__main__":
    main()