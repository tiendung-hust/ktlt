class randomLCG:
    def __init__(self, seed):
        #Bộ hệ số LCG của Numerical Recipes
        self.state=seed
        self.a= 1664525
        self.c=1013904223
        self.m= 2**32
    
    #Trả về một số trong khoảng từ low đến high
    def next(self,low,high): 
        self.state=(self.a * self.state + self.c) % self.m
        return low + (self.state % (high-low))


#Hàm xáo trộn câu hỏi, bốc câu hỏi bất kì
def shuffle(arr, seed):
    rdm=randomLCG(seed)
    #Sao chép để bảo vệ dữ liệu mảng gốc
    shuffled=list(arr)
    n = len(shuffled)
    for i in range(n-1,0,-1):
        j= rdm.next(0,i+1)
        shuffled[i],shuffled[j]=shuffled[j],shuffled[i]
    return shuffled


#Hàm sắp xếp theo điểm từ kết quả thi, key là score, nhận dữ liệu từ results.json
def bubble_sort(arr, key):
    n=len(arr)
    #Sao chép để bảo vệ dữ liệu mảng gốc
    sorted_arr=list(arr)
    for i in range(n):
        for j in range(n-i-1):
            if key(sorted_arr[j])<key(sorted_arr[j+1]):
                sorted_arr[j],sorted_arr[j+1]=sorted_arr[j+1],sorted_arr[j]
    return sorted_arr