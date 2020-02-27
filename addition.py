# addition.py
  
import random 
import sys

studentName = input("Hi! What is your name? ")
print ("Hi, " + studentName + "! Let's do some math today. Let's start with addition.")
print("You can take a break by typing \"bye\" instead of a number")

emojiDictionary = { 
	"0": "0️⃣",
	"1": "1️⃣", 
	"2": "2️⃣",
	"3": "3️⃣",
	"4": "4️⃣",
	"5": "5️⃣",
	"6": "6️⃣",
	"7": "7️⃣",
	"8": "8️⃣",
	"9": "9️⃣",
} 

def convertToEmoji(addend):
	emojiString = ""
	for num in addend:
		emojiString = emojiString + emojiDictionary.get(num, "nothing") + " "
	return emojiString

print("")

while 1:
	var1 = random.randint(1, 50)
	var2 = random.randint(1, 50)
	sum = var1 + var2
	guess = "0"
	while 1:
		print(str(var1).rjust(10))
		print("+".ljust(10))
		print(str(var2).rjust(10))
		print("==========")
		#print(questionPrompt.rstrip())
		#print("var1 length is ")
		#print(len(convertToEmoji(str(var1))))
		#print("var2 length is ")
		#print(len(convertToEmoji(str(var2))))
		guess = input("      ? ")
		if guess == "bye":
			print("\n👋 Goodbye\n")
			sys.exit()
		elif int(guess) == sum:
			print("\n✅ You got it right!\n")
			break
		else:
			print("\n❌ Sorry, that's not correct\n")

