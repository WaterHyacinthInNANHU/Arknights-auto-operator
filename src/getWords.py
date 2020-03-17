from aip import AipOcr


def baiduOCR(picfile,APP_ID,API_KEY,SECRECT_KEY):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

    with open(picfile, 'rb') as file:
        img = file.read()
        message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
        # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费

    print(message)
    return message.get('words_result')[0].get('words')

if __name__ == "__main__":

    pass