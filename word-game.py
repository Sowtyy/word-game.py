#Version: 1.3.0
#Date: 18.11.2023
#Author: Sowtyy


import json
import random


WORDS_PATH = "./russian-nouns.json"
COMMAND_PREFIX = "!"


def readJson(path : str):
  with open(path, "r", encoding = "utf-8") as file:
    return json.load(file)

def upperFirstCharLowerElse(text : str):
  return f"{text[0].upper()}{text[1:].lower()}"

def getAvailableWords(*, searchChar : str, usedWords : list[str], words : list[dict[str, list[str] | str | int | bool]]):
  availableWords : list[str] = []

  for wordDict in words:
    word = wordDict["bare"]
    
    if word.startswith(searchChar) and word not in usedWords:
      availableWords.append(word)
  
  return availableWords

def getAvailableWord(*, searchChar : str, usedWords : list[str], words : list[dict[str, list[str] | str | int | bool]]):
  availableWords = getAvailableWords(searchChar = searchChar, usedWords = usedWords, words = words)
  
  if not availableWords:
    return ""
  
  return random.choice(availableWords)

def getWordSearchChar(word : str):
  charIgnoreList = ["ь", "ы"]
  char = ""
  reverseCharIndex = 0

  while not char:
    reverseCharIndex -= 1
    char = word[reverseCharIndex]

    if char in charIgnoreList:
      char = ""
    
  return char

def askInput(text = ""):
  inp = ""

  while not inp:
    inp = input(text)
  
  return inp

def main():
  words : list[dict[str, list[str] | str | int | bool]] = readJson(WORDS_PATH)
  usedWords : list[str] = []
  wordSearchChar = ""
  lastWord = ""

  print(f"""
        Команды:
        {COMMAND_PREFIX}п - Подставить слово и пропустить ход.
        {COMMAND_PREFIX}с - Статистика.
        """)

  while True:
    wordInput = askInput(f"Ваша очередь. Напишите слово начинающееся на {wordSearchChar.upper() if wordSearchChar else 'любую букву'}: ").lower()

    if wordInput.startswith(COMMAND_PREFIX):
      command = wordInput[len(COMMAND_PREFIX):]
      if command == "п": # подставить слово
        wordInput = getAvailableWord(searchChar = wordSearchChar, usedWords = usedWords, words = words)
        if not wordInput:
          print("Я больше не знаю подходящих слов... Похоже вы выйграли!")
          break
        print(f"Подставил за вас слово {upperFirstCharLowerElse(wordInput)}.")
      elif command == "с":
        print(f"Всего использовано слов: {len(usedWords)}.")
        continue
      else:
        print("Такой команды не существует.")
        continue

    if wordSearchChar and wordInput[0] != wordSearchChar:
      print(f"Слово {upperFirstCharLowerElse(wordInput)} не начинается на букву {wordSearchChar.upper()}!")
      continue
    if wordInput in usedWords:
      print(f"Слово {upperFirstCharLowerElse(wordInput)} уже использовалось, напишите другое.")
      continue

    usedWords.append(wordInput)
    wordSearchChar = getWordSearchChar(wordInput)
    #lastWord = wordInput

    newWord = getAvailableWord(searchChar = wordSearchChar, usedWords = usedWords, words = words)

    if not newWord:
      print("Я больше не знаю подходящих слов... Похоже вы выйграли!")
      break

    print(f"{upperFirstCharLowerElse(newWord)}.")

    usedWords.append(newWord)
    wordSearchChar = getWordSearchChar(newWord)
    lastWord = newWord
  
  return

if __name__ == "__main__":
  main()
  input()
