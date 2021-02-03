import urllib.parse, http.client, json
import requests
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from io import BytesIO
from os import environ

ocr_key = "aaafdfa6aeb249cbbaa52a601eca7a6f"
ocr_endpoint = "license-plate-extraction.cognitiveservices.azure.com"
# ocr_url = "https://cdni.autocarindia.com/ExtraImages/20180402113123_NumberPlate_Swift.jpg"  
# ocr_url = "https://www.team-bhp.com/forum/attachments/travelogues/1226186d1396513427-desert-odyssey-duster-rajasthan-d4.jpg"

ocr_url = "https://st4.depositphotos.com/1592314/30923/i/1600/depositphotos_309232550-stock-photo-undefined-text-english-words-handwritten.jpg"

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': ocr_key
}

body = {
    "url": ocr_url
}

params = urllib.parse.urlencode({
    'language': 'en'
    # 'detectOrientation': 'true'
})

try:
    ocr_conn = http.client.HTTPSConnection(ocr_endpoint)
    ocr_conn.request("POST", "/vision/v3.1/read/analyze?%s" % params, str(body), headers)
    ocr_response = ocr_conn.getresponse()
    data = ocr_response.read()
    analyze_url1 = ocr_response.headers['Operation-Location']
    analyze_url = analyze_url1[8:]
    print(analyze_url)
    ocr_conn.close()
    conn = http.client.HTTPSConnection(analyze_url)
    conn.request("GET", "?%s" % params, "", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
    # data = json.loads(ocr_response.read())
    # print(json.dumps(data, indent=1))
    # ocr_conn.close()

    # image = Image.open(BytesIO(requests.get(ocr_url).content))
    # draw = ImageDraw.Draw(image)
    # boundary_color = "yellow"
    
    # environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    # environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    # environ["QT_SCALE_FACTOR"] = "1"

    # for boundary in data['regions']:
    #     region_box = boundary['boundingBox']
    #     coordinates = region_box.split(',')
    #     left = int(coordinates[0])
    #     top = int(coordinates[1])
    #     width = int(coordinates[2])
    #     height = int(coordinates[3])
    #     draw.line([(left, top), (left + width, top)], fill = boundary_color, width=10)
    #     draw.line([(left, top), (left, top + height)], fill = boundary_color, width = 10)
    #     draw.line([(left, top + height), (left + width, top + height)], fill = boundary_color, width = 10)
    #     draw.line([(left + width, top + height), (left + width, top)], fill=boundary_color, width=10)
        
    #     for lines in boundary['lines']:
    #         for words in lines['words']:
    #             print(words['text'])

    # plt.imshow(image)
    # plt.show()

except Exception as e:
    print("We have error: ")
    print(e)