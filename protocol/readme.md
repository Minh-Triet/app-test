# How to generate code from CMS API protocol files

1. CMS API protocol are in [proto](./proto) folder.

    *NOTE: file structure must be preserved.*
2. Extract bin/protoc.exe from corresponding *.zip* archive to this folder.

3. Run [generate.cmd](generate.cmd) (Windows).

    *NOTE: By default generated files are located in [this](../client/proto) folder.*

To generate code for other supported languages (for example C#),
in [generate.cmd](generate.cmd) replace *python_out* with *selected_language_out* (for example *csharp_out*).

*NOTE: protoc archives come from: https://github.com/protocolbuffers/protobuf/releases
