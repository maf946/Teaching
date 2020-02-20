# url.py

# import a library of code used to create the HTTP request
import urllib.request

# get input from the user, then store the result in a variable named "url"
url = input("Which page would you like to load? ")

# send the HTTP request, and store the results in a collection of bytes called "f"
f = urllib.request.urlopen(url)

# decode the bytes as text, and print them to the screen
print(f.read().decode('utf-8'))