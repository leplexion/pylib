from math import floor
from PIL import Image as ImageModule
from PIL.Image import Image
import io

'''
- 官方文档
https://pillow.readthedocs.io/en/stable/

- PIL 支持的 format 格式
https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
'''

class Size:
    def __init__(self, w:int, h: int) -> None:
        self.w:int = w
        self.h:int = h
    def __str__(self)->str:
        return f'{{"w": {self.w}, "h": {self.h}}}'

'''----------------------------------------------------'''
def im_from_file(path:str)->Image:
    return ImageModule.open(path) 

def im_from_file_raw(raw:bytes)->Image:
    '''从图片文件的bytes数据读入image'''
    return Image.frombytes(raw)

def im_to_file(im:Image, path:str, f:str='PNG'):
    '''将图片对象保存到文件'''
    im.save(path, format=f)

def im_to_file_raw(im:Image, f:str='PNG')->bytes:
    '''将图片转为bytes'''
    bio = io.BytesIO()
    im.save(bio, format=f)
    return bio.getvalue()


'''----------------------------------------------------'''
def im_show(im:Image):
    '''该方法会将写入临时文件, 并直接打开'''
    im.show()

'''----------------------------------------------------'''
def im_zoom_rate(im:Image, rate:float, resample=None, box=None, reducing_gap:float=None)->Image:
    '''按比例缩放'''
    size = im_get_size(im)
    w = floor(size.w * rate)
    h = floor(size.h * rate)
    im_resize(im, w, h, resample, box, reducing_gap)
    return im

def im_resize(im:Image, w:int, h:int, resample=None, box=None, reducing_gap:float=None):
    '''重置image的尺寸'''
    im.resize((w, h), resample, box, reducing_gap)
    pass

def im_resize2(im:Image, size:Size, resample=None, box=None, reducing_gap:float=None):
    im_resize(im, size.w, size.h, resample, box, reducing_gap)

def im_zoom_adapt_rect(im:Image, w:int, h:int, resample=None, box=None, reducing_gap:float=None):
    '''让图片适应一个尺寸做缩放, 返回中心点坐标和新尺寸'''
    size = im_get_size(im)

    size.w
    size.h

    pass

'''----------------------------------------------------'''
def im_data(im:Image)->list:
    '''一维列表[(r,g,b), (r,g,b)]'''
    return im.getdata()


def im_get_width(im:Image)->int:
    return im.size[0]

def im_get_height(im:Image)->int:
    return im.size[1]



def im_get_size(im:Image)->Size:
    s = im.size
    return Size(w=s[0], h=s[1])




if __name__ == '__main__':
    im = im_from_file('C:\\Users\\DY-I7\\Desktop\\bcd.jpg')
    print(im_get_size(im))
    pass