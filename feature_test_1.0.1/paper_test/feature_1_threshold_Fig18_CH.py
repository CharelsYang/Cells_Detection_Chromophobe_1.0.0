import cv2 as cv
import matplotlib.pyplot as plt
def MaxMinNormalization(x,Max,Min):
    x = (x - Min) / (Max - Min);
    return x;
def loop(file):
    img = cv.imread("G:\\2020summer\\Project\\Chromophobe_dataset1\\single_cells_chromophobe\\"+str(file)+".jpg")
    cv.imshow("img", img)
    print("img size: ",img.shape[0],img.shape[1])
    # img=cv.cvtColor(img,cv.COLOR_BGR2BGRA)

    img_masked = img.copy()
    img_nucleus_white_img = img.copy()

    # -----preprocess-----
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow("gray", gray)

    gauss = cv.GaussianBlur(gray, (5, 5), 5)
    # cv.imshow("gauss1",gauss)
    def cnt_area(cnt):
        area = cv.contourArea(cnt)
        return area
    thresh_histgram=[]
    area_list = []

    start_value=100
    end_value=230
    for i in range(start_value,end_value):

        area_size_list=[]
        print("正在进行第:",i)
        ret, thresh = cv.threshold(gauss, i, 255, 0)
        erode = cv.erode(thresh, None, iterations=2)
        #cv.imshow("thresh", thresh)
        cnts, hierarchy = cv.findContours(erode.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        temp_list=[]

        area_count=0
        for t in range(img.shape[0]):
            for y in range(img.shape[1]):
                if erode[t][y]==0:

                    area_count+=1
        area_list.append(area_count)

        number_of_cells_list=[]
        for x in range(0,500):
            number_of_cells=0
            for m in cnts:
                if 200 <= cnt_area(m) <= 0.8*(img.shape[0]*img.shape[0]):
                    temp_list.append(m)
                if cnt_area(m) <= 0.8*(img.shape[0]*img.shape[0]):

                    area_size_list.append(cnt_area(m))
                if x <= cnt_area(m) <= 0.8*(img.shape[0]*img.shape[0]):
                    number_of_cells+=1
            number_of_cells_list.append(number_of_cells)
        thresh_histgram.append(len(temp_list))


    """plt.plot(range(0,len(number_of_cells_list),1),number_of_cells_list)
    plt.title("number of cells")
    
    plt.show()
    plt.plot(range(start_value,start_value+len(thresh_histgram),1),thresh_histgram)
    #plt.axvline(192)
    plt.show()
    """

    #normalization
    max_list=max(area_list)
    min_list = min(area_list)
    area_list_normalized=[]
    for i in area_list:
        a=MaxMinNormalization(i,max_list,min_list)
        area_list_normalized.append(a)

    #print(area_list)
    plt.plot(range(start_value,start_value+len(area_list),1),area_list_normalized)
#plt.axvline(192)

for i in range(1,9):
    print("正在处理第 ",i," 张图......")
    loop(i)
plt.legend(['Sample: 1', 'Sample: 2','Sample: 3','Sample: 4','Sample: 5','Sample: 6','Sample: 7','Sample: 8','9','10'], prop={'size': 15})
font1 = {
    'weight': 'normal',
    'size': 20,
}

plt.tick_params(labelsize=15)
plt.xlabel('Threshold', font1)
plt.ylabel('The ratio of black pixels', font1)
plt.show()


cv.waitKey()