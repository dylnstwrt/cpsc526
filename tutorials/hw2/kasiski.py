import sys

ASCII_SIZE = 128
  
def getMaxOccuringChar(str): 
    # Create array to keep the count of individual characters 
    # Initialize the count array to zero 
    count = [0] * ASCII_SIZE 
  
    # Utility variables 
    max = -1
    c = '' 
  
    # Traversing through the string and maintaining the count of 
    # each character 
    for i in str: 
        count[ord(i)]+=1; 
  
    for i in str: 
        if max < count[ord(i)]: 
            max = count[ord(i)] 
            c = i 
  
    return c 

def getDivisors(n):
    l = []
    for i in range(2,n):
        if n % i == 0:
            l.append(i)
    return l


def main():
    ct = open("transmission3")
    c_bytes = ct.read()
    ct.close()

    length = c_bytes.__len__()

    #something to store substrings that have already been counted
    counted = set()
    distances = dict()

    # search for 3-tuples
    for i in range(length-3):


        bound = i+3
        substring = c_bytes[i:bound]
        count = c_bytes.count(substring)

        if substring in counted:
            continue
        counted.add(substring)

        # the instances of distances occuring
        index = bound
        if count > 1:
            for j in range(count - 1):
                index = c_bytes.find(substring, index)
                if distances.__contains__(index - i):
                    d1 = {index-i: distances.get(index-i) + 1}
                    distances.update(d1)
                else:
                    distances.update({index-i: 1})
    
    factorFreq = dict()
    for key in distances.keys():
        factors = getDivisors(key)
        for factor in factors:
            if factorFreq.__contains__(factor):
                d = {factor: factorFreq.get(factor)+1}
                factorFreq.update(d)
            else:
                factorFreq.update({factor: 1})

    print("Probable Key Length:", max(factorFreq, key=factorFreq.get))
    keyLength = max(factorFreq, key=factorFreq.get)
    counted.clear()
    distances.clear()

    key = ""
    for j in range(keyLength):
        column = "";
        for i in range(j, length, keyLength):
            column += c_bytes[i]
        
        mostFreq = getMaxOccuringChar(column)
        key += chr(ord('E') ^ ord(mostFreq))
    
    print("Key assuming probable key length:",key)

    msgstream = ""
    for i in range(length):
        msgstream += chr(ord(c_bytes[i]) ^ ord(key[i%5]))

    print("Plaintext using key:",msgstream)


if __name__ == "__main__":
    main()