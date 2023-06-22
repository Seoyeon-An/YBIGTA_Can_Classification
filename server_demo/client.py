import logging
import os
import grpc
from protos import hello_pb2, hello_pb2_grpc


def get_filepath(filename, extension):
    return f'{filename}{extension}'


def read_iterfile(filepath, chunk_size=1024):
    split_data = os.path.splitext(filepath)
    filename = split_data[0]
    extension = split_data[1]

    metadata = hello_pb2.MetaData(filename=filename, extension=extension)
    yield hello_pb2.UploadFileRequest(metadata=metadata)
    with open(f'server/resources/{filepath}', mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                entry_request = hello_pb2.UploadFileRequest(chunk_data=chunk)
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                return


def run():
    with grpc.insecure_channel('34.64.40.136:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)

        # say hello
        # response = stub.SayHello(
        #     hello_pb2.HelloRequest(name='John Doe', age=30))
        # print("Greeter client received: " + response.message)

        # upload file: given an file (txt/img), reads it as byte sequence and returns one str message.
        response = stub.UploadFile(read_iterfile('hotsix_test.jpg'))
        print("Greeter client received: " + response.message)

        # download file: given a filename, downloads and saves as file
        # filename = 'test'
        # extension = '.jpg'
        # filepath = get_filepath(filename, extension)
        # for entry_response in stub.DownloadFile(hello_pb2.MetaData(filename=filename, extension=extension)):
        #     with open("download_result.jpg", mode="ab") as f:
        #         f.write(entry_response.chunk_data)
        # print("Downloaded image successfully.")


if __name__ == '__main__':
    logging.basicConfig()
    run()
