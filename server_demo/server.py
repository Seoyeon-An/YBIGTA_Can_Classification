from concurrent import futures
import logging
import os
import io
import grpc
from PIL import Image
from protos import hello_pb2, hello_pb2_grpc

from ultralytics import YOLO
import torch
import numpy as np


def get_filepath(filename, extension):
    return f'{filename}{extension}'


def run(image):
    model = YOLO('./model.pt')
    result = model.predict(image)
    answer = result[0].names[result[0].probs.top1]
    # threshold = result[0].probs.top1conf
    # return [answer, threshold]
    return answer


class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.StringResponse(
            message=f'Hello, {request.name}! Your age is {request.age}')

    def UploadFile(self, request_iterator, context):
        data = bytearray()
        filepath = 'dummy'

        for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = get_filepath(
                    request.metadata.filename, request.metadata.extension)
                newsavepath = f'uploads/{request.metadata.filename}1{request.metadata.extension}'
                continue
            data.extend(request.chunk_data)

        image = Image.open(io.BytesIO(data))
        image.save('restored.png')

        result = run(image)

        # Prints the uploaded text in the server terminal
        # print(data.decode())

        # Writes the uploaded data into file in server
        # Disclaimer: need to create folder beforehand otherwise "File does not exist error happens"
        # with open(newsavepath, 'wb') as f:
        #     f.write(data)

        # Returns Success! once the file was properly uploaded to the server.
        # return hello_pb2.StringResponse(message='Successfully uploaded!')
        return hello_pb2.StringResponse(message=result)

    def DownloadFile(self, request, context):
        chunk_size = 1024

        filepath = f'server/resources/{request.filename}{request.extension}'
        if os.path.exists(filepath):
            with open(filepath, mode="rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:
                        entry_response = hello_pb2.FileResponse(
                            chunk_data=chunk)
                        yield entry_response
                    else:
                        return


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
