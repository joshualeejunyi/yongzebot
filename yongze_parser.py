import telegram

def get_bot_key():
    api_key = ''
    with open("botapi.txt", "r") as f:
        api_key = f.read() 
    
    return api_key

def main():
    api_key = get_bot_key() 
    bot = telegram.Bot(token=api_key) 
    cancer = input()
    cancer_list = cancer.split(" ")
    cancer_is_gone = list()

    for word in cancer_list:
        word = word.lower()
        if word in yongze_dictionary.keys():
            cancer_is_gone.append(yongze_dictionary[word])
        else:
            cancer_is_gone.append(word)
    

    print("This is the non-cancer version:\n")
    print(" ".join(cancer_is_gone))

if __name__ == "__main__":
    main()