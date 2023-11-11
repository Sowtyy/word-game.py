#Version: 1.1.0
#Date: 11.11.2023
#Author: Sowtyy


import json
import random


WORD_DICT_PATH = "./russian_nouns_with_definition.json"


def readJson(path : str):
  with open(path, "r", encoding = "utf-8") as file:
    return json.load(file)

def upperFirstChar(text : str):
  return f"{text[0].upper()}{text[1:]}"

def getWordDefinition(word : str, wordDict : dict[str, str]):
  return wordDict[word]["definition"]

def wordIsPlural(word : str, wordDict : dict[str, str]):
  if "мн. " in getWordDefinition(word, wordDict):
    return True
  return False

def getWordSearchChar(word : str):
  charIgnoreList = ["ь"]
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
  wordDict : dict[str, str] = readJson(WORD_DICT_PATH)
  usedWords = []
  wordSearchChar = ""
  lastWord = ""

  while True:
    wordInput = askInput(f"Ваша очередь. Напишите слово начинающееся на {wordSearchChar.upper() if wordSearchChar else 'любую букву'}: ").lower()

    if wordInput == "!з":
      if not lastWord:
        print("Ни одно слово ещё не было написано.")
        continue
      print(f"Значение слова {lastWord}: {getWordDefinition(lastWord, wordDict)}")
      continue
    if wordSearchChar and wordInput[0] != wordSearchChar:
      print(f"Слово {wordInput} не начинается на букву {wordSearchChar.upper()}!")
      continue
    if wordInput in usedWords:
      print(f"Слово {upperFirstChar(wordInput)} уже использовалось, напишите другое.")
      continue

    usedWords.append(wordInput)
    wordSearchChar = getWordSearchChar(wordInput)
    #lastWord = wordInput

    wordsStartingWithChar = [word for word in wordDict
                             if word.startswith(wordSearchChar)
                             and word not in usedWords
                             and not wordIsPlural(word, wordDict)]

    if not wordsStartingWithChar:
      print("Вы выйграли! Каким-то образом...")
      break

    newWord = random.choice(wordsStartingWithChar)

    print(f"{upperFirstChar(newWord)}.")

    usedWords.append(newWord)
    wordSearchChar = getWordSearchChar(newWord)
    lastWord = newWord
  
  return

if __name__ == "__main__":
  main()
  input()
