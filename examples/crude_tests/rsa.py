import random
import math

def main():
	#details of a
	#p = int(input())
    pa = 5
    #q = int(input())
    qa = 7
    na = da = ea = 0
    na, da, ea = set_keys_A(pa, qa)
    pka = [ea, na] #public key
    ska = [da, na] #private(secret) key
    Na = random.randrange(1, 20)
    A_nonceA = -1
    A_nonceB = -1
    

    #details of b
    #p = int(input())
    pb = 3
    #q = int(input())
    qb = 7
    nb = db = eb = 0
    nb, db, eb = set_keys_B(pb, qb)
    pkb = [eb, nb] #public key
    skb = [db, nb] #private(secret) key
    Nb = random.randrange(1, 20)
    B_nonceA = -1
    B_nonceB = -1
    

    #Communication begins
    CipherNa = encode(nb, eb, Na)
    #print("2. Encrypted msgA :"+str(CipherA)+"\n"+"Encrypted Na :"+str(CipherNa)+"\n")

    #print("3. B decrypts  using his private key : \n")
    #DecryptedA = decode(nb, db, CipherA)
    DecryptedNa = decode(nb, db, CipherNa)
    #msgReceiverB[0]["message"] = DecryptedA
    B_nonceA = DecryptedNa
    
    #print(" A sent the details msgA : "+str(msgReceiverB[0]["message"])+" to B with nonceA: "+str(msgReceiverB[1]["nonceA"])+"\n")

    #print("\n4. B encrypts the msgB, nonceA and nonceB using public key of A \n ")
    CipherNb = encode(na, ea, Nb)
    CipherNa = encode(na, ea, Na)
    # print("5. Encrypted msgB :"+str(CipherB)+"\n"+"Encrypted Nb :"+str(CipherNb)+" Encrypted Na :"+str(CipherNa))
    
    # print("\n6.A decrypts msgB using his private key : \n")
    #DecryptedB = decode(na, da, CipherB)
    #DecryptedNb = decode(na, da, CipherNb)
    DecryptedNa = decode(na, da, CipherNa)
    A_nonceB = DecryptedNb
    A_nonceA = DecryptedNa
    # msgReceiverA[0]["message"] = DecryptedB
    # msgReceiverA[1]["nonceA"] = DecryptedNa
    # msgReceiverA[2]["nonceB"] = DecryptedNb
    # print("7. B sent the details msgB : "+str(msgReceiverA[0]["message"])+" to A with nonceA: "+str(msgReceiverA[1]["nonceA"])+" with nonceB :"+str(msgReceiverA[2]["nonceB"])+"\n")


    if DecryptedNa == Na:
        print("A received the same nonce back from B")
    else:
        print("A did not receive the same nonce back from B")

    CipherNb = encode(nb, eb, Nb)
    DecryptedNb = decode(nb, db, CipherNb)
    B_nonceB = DecryptedNb
    # print("8. B received nonceB as"+str(msgReceiverB[2]["nonceB"])+" from A");
    
    if Nb == DecryptedNb:
        print("B received the same nonce back from A")
    else:
        print("B did not receive the same nonce back from A")

#end of main function

#function to encode the message
def encode(n, e, M):
    return (M ** e) % n

def decode(n, d, C):
    return (C ** d) % n

#function to produce the keys
def set_keys_A(p, q):
	#p and q two large prime numbers
    

    n = p * q
    phi = (p-1) * (q-1)
    e = 5
    # print (" e =  " + str(e))
    #d = (k * phi) + 1 / efor some integer k
    d = 5 #for k = 2

    return [n, d, e]

def set_keys_B(p, q):
	#p and q two large prime numbers
    

    n = p * q
    phi = (p-1) * (q-1)
    e = 5
    # print (" e =  " + str(e))
    #d = ((2 * phi) + 1 )/ e
    d = 5 #for k = 2

    return [n, d, e]

def get_e(phi):
    p = 0
    for i in range(2, phi):
        p = gcd(i, phi)
        if p == 1 :
            break
    return i

def gcd(a, b):
    if a == 0 :
        return b
    p = b % a
    q = a
    return gcd(p, q)


main()