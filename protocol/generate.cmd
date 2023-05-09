call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\CMS\cmsapi_1.proto
call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\CMS\common_1.proto
call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\CMS\traderouting_1.proto
call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\common\shared_1.proto
call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\common\decimal.proto
call protoc.exe --proto_path=.\proto --python_out=..\client\proto proto\common\timestamp.proto