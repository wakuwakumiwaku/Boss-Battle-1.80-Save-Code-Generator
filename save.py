import random
import stringcase


playername: str = input("Enter your username (casesensitive): ")
lvl: int = int(input(" Enter the lvl you want to restore (between 0 and 100): "))
exp: int = int(input("Enter the amount of xp you want to restore: "))


string: str = ""
finstring: str = ""
enstring: str = ""
key: str
char: str
k: int
km: int
j: int
jm: int
saveslot: list[int] = [0 for x in range(0, 3)]
savedivideint: int
saveremainder: int
sumint: int = 0

encryptionnumbers: list[str] = [0 for x in range(0, 36)]
savetempstrings: list[str] = [0 for x in range(0, 36)]
savecharnums: list[str] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
encryptionset: list[str] = [0 for x in range(0, 7)]

saveLoadCharacterSet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
encryptionset[1] = "JCYVQSB71EXK65WZ0LTA2POM8UIRHD43N9FG"
encryptionset[2] = "A09UYH1R3CMZBK4DQ8OTS5LVIXPF7NGJ2E6W"
encryptionset[3] = "92QXCID71KOLZ0PH6UWNMTB5GS38VJERAFY4"
encryptionset[4] = "7MWYO49IVESG10ZC2NUTQ8AJFXR6K5BHDLP3"
encryptionset[5] = "JU9RAWQYL4ICP73K8OSFM1BTN6EXVD025GHZ"
encryptionset[6] = "YXN70HR64ZBG9UIJE3DWS5TOPCLMAKF2V81Q"

saveslot[1] = 4
saveslot[2] = 2


k = 1
km = 35
while k <= km:
    encryptionnumbers[k] = ""
    k = k + 1


k = 1
while k <= 2:
    savetempstrings[k] = ""
    k = k + 1


keyint = random.randint(1, 6)
key = savecharnums[keyint]
# test
# key = 3


k = 1
km = 36
while k <= km:
    encryptionnumbers[k - 1] = encryptionset[keyint][k - 1 : k]
    k = k + 1


l = 1
while l <= 2:
    if l == 1:
        con = exp
    if l == 2:
        con = lvl
    k = 1
    km = saveslot[l]
    while k <= km:
        savepowermax = 1
        j = k
        jm = saveslot[l] - 1
        while j <= jm:
            savepowermax = savepowermax * 36
            j = j + 1
        if saveslot[l] - k >= 1:
            savedivideint = int(con / savepowermax)
            saveremainder = int(con - (savedivideint * savepowermax))

            savetempstrings[l] = savetempstrings[l] + savecharnums[savedivideint]
        else:
            savetempstrings[l] = savetempstrings[l] + savecharnums[saveremainder]
        con = saveremainder
        k = k + 1
    l = l + 1

k = 1
while k <= 2:
    enstring = enstring + savetempstrings[k]
    k = k + 1


k = 1
km = len(enstring)
while k <= km:
    j = 0
    jm = 35
    while j <= jm:
        if enstring[k - 1 : k] == savecharnums[j]:
            sumint = sumint + j
        j = j + 1
    k = k + 1

con = sumint


savedivideint = int(con / 36)
saveremainder = int(con - (savedivideint * 36))
char = savecharnums[saveremainder]
enstring = enstring + char
name = len(playername)

k = 1
while k <= 2:
    j = 1
    jm = 36
    while j <= jm:
        if playername[k - 1 : k] == encryptionset[1][j - 1 : j]:
            name = name + j
        j = j + 1
    k = k + 1

con = name
savedivideint = int(con / 36)
saveremainder = int(con - (savedivideint * 36))
char = savecharnums[saveremainder]
enstring = enstring + char

k = 1
km = len(enstring)
while k <= km:
    j = 0
    jm = 35
    while j <= jm:
        if enstring[k - 1 : k] == savecharnums[j]:
            string = string + encryptionset[keyint][j]
        j = j + 1
    con = k
    savedivideint = int(con / 6)
    saveremainder = int(con - (savedivideint * 6))
    if saveremainder <= 0:
        string = string + "-"
    k = k + 1
finstring = str.join("", (key, "-", string))

print(finstring)
