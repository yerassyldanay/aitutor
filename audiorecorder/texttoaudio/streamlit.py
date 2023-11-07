import pyttsx3
engine = pyttsx3.init()

# Set the properties for the converter
engine.setProperty('rate', 150)  # Sets speed percent
engine.setProperty('volume', 0.7)  # Set volume 0-1

engine.say("Imagine you're in a magical library that's unlike any other. In a regular library, to find a book, you'd have to check each aisle one by one until you find your book. That's kind of like how classical computers work, dealing with one bit of information at a time, represented as either 0s or 1s. Now, in this magical library, you have a special pair of glasses. When you wear them, you don't see just one reality, you see multiple realities, all layered on top of each other, all the different aisles and books at once. In one reality, you're picking up a book of recipes, in another, you're reading a mystery novel, and in yet another, you're referencing an encyclopedia. This is similar to how quantum computers work.")
engine.runAndWait()