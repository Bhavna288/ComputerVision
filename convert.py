from azure_data import cog_endpoint, cog_key
print('Ready to use cognitive services at {} using key {}'.format(cog_endpoint, cog_key))

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image
import time
import os

# %matplotlib inline

def extractText(file_name):

    # Read the image file
    image_path = os.path.join('uploads', file_name)
    image_stream = open(image_path, "rb")
    resultString = ""

    # Get a client for the computer vision service
    computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

    # Submit a request to read printed text in the image and get the operation ID
    read_operation = computervision_client.read_in_stream(image_stream, raw=True)
    operation_location = read_operation.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the asynchronous operation to complete
    while True:
        read_results = computervision_client.get_read_result(operation_id)
        if read_results.status not in [OperationStatusCodes.running]:
            break
        time.sleep(1)

    # If the operation was successfuly, process the text line by line
    if read_results.status == OperationStatusCodes.succeeded:
        for result in read_results.analyze_result.read_results:
            for line in result.lines:
                resultString += line.text + "\n"
                print(line.text)

    return resultString

def extractFromHandwritten(file_name):
    # Read the image file
    image_path = os.path.join('uploads', file_name)
    image_stream = open(image_path, "rb")
    resultString = ""

    # Get a client for the computer vision service
    computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

    # Submit a request to read printed text in the image and get the operation ID
    read_operation = computervision_client.read_in_stream(image_stream, raw=True)
    operation_location = read_operation.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the asynchronous operation to complete
    while True:
        read_results = computervision_client.get_read_result(operation_id)
        if read_results.status not in [OperationStatusCodes.running]:
            break
        time.sleep(1)

    # If the operation was successfuly, process the text line by line
    if read_results.status == OperationStatusCodes.succeeded:
        for result in read_results.analyze_result.read_results:
            for line in result.lines:
                resultString += line.text + "\n"
                print(line.text)
    
    return resultString
