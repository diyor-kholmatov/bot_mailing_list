joinedFile = open("joined.txt", "r")
joinedUsers = set()

for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()
