# def Dcm2jpg(file_path):
#     # 获取所有图片名称
#     names = os.listdir(file_path)  # 路径
#     # 将文件夹中的文件名称与后边的 .dcm分开
#
#     for files in names:
#         picture_path = "./1527/" + files
#         out_path = "./1527out/" + files + ".jpg"
#         ds = pydicom.read_file(picture_path)
#         img = ds.pixel_array  # 提取图像信息
#         scipy.misc.imsave(out_path, img)
#
#     print('all is changed')
#
#
# Dcm2jpg('./1527')
import SimpleITK as sitk
import numpy as np
import cv2
import os
def convert_from_dicom_to_jpg(img,low_window,high_window,save_path):
    lungwin = np.array([low_window*1.,high_window*1.])
    newimg = (img-lungwin[0])/(lungwin[1]-lungwin[0])    #归一化
    newimg = (newimg*255).astype('uint8')                #将像素值扩展到[0,255]
    cv2.imwrite(save_path, newimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])



if __name__ == '__main__':

    # 下面是将对应的dicom格式的图片转成jpg
    dcmpath = './1527'       #读取dicom文件

    names = os.listdir(dcmpath)
    for file in names:
        dcm_image_path = "./1527/" + file
        output_jpg_path = "./1527out/" + file + ".jpg"

        ds_array = sitk.ReadImage(dcm_image_path)         #读取dicom文件的相关信息
        img_array = sitk.GetArrayFromImage(ds_array)      #获取array
        # SimpleITK读取的图像数据的坐标顺序为zyx，即从多少张切片到单张切片的宽和高，此处我们读取单张，因此img_array的shape
        #类似于 （1，height，width）的形式
        shape = img_array.shape
        img_array = np.reshape(img_array, (shape[1], shape[2]))  #获取array中的height和width
        high = np.max(img_array)
        low = np.min(img_array)
        convert_from_dicom_to_jpg(img_array, low, high, output_jpg_path)   #调用函数，转换成jpg文件并保存到对应的路径
        print('FINISHED')
