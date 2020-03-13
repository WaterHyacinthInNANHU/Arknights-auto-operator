from aip import AipOcr


def baiduOCR(picfile,APP_ID,API_KEY,SECRECT_KEY):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

    # i = open(picfile, 'rb')#图片转换为字节流
    # img = i.read()
    # message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
    # # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    # print("识别成功！")
    # i.close()

    with open(picfile, 'rb') as file:
        img = file.read()
        message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费
        # message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费

    # with open(outfile, 'a+') as fo:
    #     fo.writelines("+" * 60 + '\n')
    #     fo.writelines("文本内容：\n")
    #     # 输出文本内容
    #     for text in message.get('words_result'):
    #         fo.writelines(text.get('words') + '\n')
    #     fo.writelines('\n' * 2)
    # print("文本导出成功！")
    print(message)
    return message.get('words_result')[0].get('words')

if __name__ == "__main__":
    print(baiduOCR("imgs\\dengjitisheng.jpg"))
    pass