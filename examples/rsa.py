import random
import math

def main():
    pka = [5, 21] #public key
    ska = [5, 21] #private(secret) key
    Na = random.randrange(1, 20)
    A_nonceA = -1
    A_nonceB = -1
    

    pkb = [5, 21] #public key
    skb = [5, 21] #private(secret) key
    Nb = random.randrange(1, 20)
    B_nonceA = -1
    B_nonceB = -1
    

    #Communication begins
    CipherNa_A = aCallsEncode(pkb, Na)
    #print("2. Encrypted msgA :"+str(CipherA)+"\n"+"Encrypted Na :"+str(CipherNa)+"\n")

    #print("3. B decrypts  using his private key : \n")
    #DecryptedA = decode(nb, db, CipherA)
    B_nonceA = bCallsDecode(skb, CipherNa_A)
    #msgReceiverB[0]["message"] = DecryptedA
    
    #print(" A sent the details msgA : "+str(msgReceiverB[0]["message"])+" to B with nonceA: "+str(msgReceiverB[1]["nonceA"])+"\n")

    #print("\n4. B encrypts the msgB, nonceA and nonceB using public key of A \n ")
    CipherNb_B = bCallsEncode(pka, Nb)
    CipherNa_B = bCallsEncode(pka, B_nonceA)
    # print("5. Encrypted msgB :"+str(CipherB)+"\n"+"Encrypted Nb :"+str(CipherNb)+" Encrypted Na :"+str(CipherNa))
    
    # print("\n6.A decrypts msgB using his private key : \n")
    #DecryptedB = decode(na, da, CipherB)
    #DecryptedNb = decode(na, da, CipherNb)
    A_nonceA = aCallsDecode(ska, CipherNa_B)
    A_nonceB = aCallsDecode(ska, CipherNb_B)
    # msgReceiverA[0]["message"] = DecryptedB
    # msgReceiverA[1]["nonceA"] = DecryptedNa
    # msgReceiverA[2]["nonceB"] = DecryptedNb
    # print("7. B sent the details msgB : "+str(msgReceiverA[0]["message"])+" to A with nonceA: "+str(msgReceiverA[1]["nonceA"])+" with nonceB :"+str(msgReceiverA[2]["nonceB"])+"\n")


    if A_nonceA == Na:
        print("A received the same nonce back from B")
    else:
        print("A did not receive the same nonce back from B")

    CipherNb_A = aCallsEncode(pkb, A_nonceB)
    B_nonceB = bCallsDecode(pkb, CipherNb_A)
    # print("8. B received nonceB as"+str(msgReceiverB[2]["nonceB"])+" from A");
    
    if Nb == B_nonceB:
        print("B received the same nonce back from A")
    else:
        print("B did not receive the same nonce back from A")

#end of main function
def aCallsEncode(list1, S):
    return encode(list1, S)

def aCallsDecode(list1, S):
    return decode(list1, S)

def bCallsEncode(list1, S):
    return encode(list1, S)

def bCallsDecode(list1, S):
    return decode(list1, S)

#function to encode the message
def encode(list1, M):
    n = list1[0]
    e = list1[1]
    t = M ** e
    f = t % n
    return f 

def decode(list1, C):
    n = list1[0]
    d = list1[1]
    t = C ** d
    f = t % n
    return f

#function to produce the keys
# def set_keys_A(p, q):
# 	#p and q two large prime numbers
    

#     n = p * q
#     phi = (p-1) * (q-1)
#     e = 5
#     # print (" e =  " + str(e))
#     #d = (k * phi) + 1 / efor some integer k
#     d = 5 #for k = 2

#     return n, d, e

# def set_keys_B(p, q):
# 	#p and q two large prime numbers
    

#     n = p * q
#     phi = (p-1) * (q-1)
#     e = 5
#     # print (" e =  " + str(e))
#     #d = ((2 * phi) + 1 )/ e
#     d = 5 #for k = 2

#     return n, d, e

main()