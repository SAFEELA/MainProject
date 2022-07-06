from ssdeep import ssdeep



def hash_function(data):
    hash1=ssdeep(data)
    return hash1

    


if __name__=="__main__":

    s1 = 'some long text'  # or open('first.txt').read()
    hash1 = spamsum(s1)
    hash2 = spamsum('somewhat long telegram')
    hash3=spamsum('some long text')


    