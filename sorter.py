def alphabetical_shortness(a, b):
    a_smaller_b = False
    
    #Get shortest name to make double nested for loop innecessary
    shr_name = len(a)
    if len(a) > len(b):
        shr_name = len(b)

    #Go through each letter to find which word goes first
    for j in range(shr_name):
        if ord(a[j]) < ord(b[j]):
            a_smaller_b = True
            break

    return a_smaller_b