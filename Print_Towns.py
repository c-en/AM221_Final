for number in range(9):
    print(number+1)
    district=np.zeros(351)
    for i in range(351):
        district[i]=z[i][number].x
    print(district) # Print vector indicating which towns are in district "number+1"
    for i in range(351):
        if district[i]==1:
            print(("'"+str(TOWNS[i])+"',").strip()) # Print list of towns in district "number+1"
