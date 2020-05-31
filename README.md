![BaMMI_Not_Bambi](https://vignette.wikia.nocookie.net/disney/images/c/ce/Profile_-_Bambi.png/revision/latest/scale-to-width-down/1031?cb=20190313173158)
[![Build Status](https://travis-ci.com/roypel/BaMMI.svg?branch=master)](https://travis-ci.com/roypel/BaMMI)
![coverage](https://codecov.io/gh/roypel/BaMMI/branch/master/graph/badge.svg)

*This project isn't related to Bambi™ in any way, except they share 80% of the letters in their name* 

# BaMMI
BaMMI is a Basic Mind-Machine Interface, designed to let you save, manage and communicate your thoughts to a machine!
How cool is that?!


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:roypel/BaMMI.git
    ...
    $ cd BaMMI/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [BaMMI] $ # Let's roll
    ```
   
   
## Usage

`BaMMI` provides access to five different components via API and command-line interface.
The five components are a client, a server, parser handler, saver
 and an API to communicate with a DB that keeps the data.

While the components can work independently, and might also integrate
 with different services that aren't provided in this package, there's a provided `run-pipeline.sh` script
 that will orchestrate all the needed backend so you could just use the client 
 (simply use `python -m BaMMI.client upload-sample /path/to/snapshot/data` after installation finishes) to upload some data and 
 see how it all works. To know all is up, a pytest tests will be launched until they pass, might take a minute or two
 until all the services are up.

Note that all the CLI commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

### Client

The client is available as `BaMMI.client` with the `upload_sample` API that given a `host`, `port`, and a `path` to 
a local snapshot file, will upload the given file in `path` to _`host:port`_.

There's also an option to upload a file through the CLI, via `python -m BaMMI.client upload-sample`, which has
the options to receive a host (_`-h`_ or _`--host`_) and a port (_`-p`_ or _`--port`_), and a path to the snapshot file.

The default values both in the API and CLI are `host='127.0.0.1'`, `port=8000`.

Note that the expected file format is a gzipped binary file that has a sequence of message sizes (uint32) and messages
of the corresponding sizes, assuming the first message is a User message and the rest are this user snapshots.

The messages are expected to contain messages as defined in [this .proto file](https://storage.googleapis.com/advanced-system-design/cortex.proto).
Also, a sample file [is available here](https://storage.googleapis.com/advanced-system-design/sample.mind.gz).
Please refrain from downloading it without any certain need.


### Server

The server is available as `BaMMI.server`, with the `run_server` API, and the `run-server` command in the CLI (`python -m cortex.server run-server`).
Both get a `host` and `port` as was in the client, and they also have the same defaults and options, while unlike the client the server gets a publish destination.

What does it mean? Well, in the API there's an option to pass a `publish` function, that any snapshot data that the server receives
will be sent to the function and handled there. On the CLI, passing a function isn't possible, however there's an option to pass 
a MQ URL (RabbitMQ is preferred currently) that the server will publish the data there, so others may consume and process it.

The expected URL format is `service-name://user:password@host:port/`, e.g. `rabbitmq://127.0.0.1:5672/`.

In case you use the CLI or the default publish function, know that the data that will be published to the MQ as a JSON,
containing `user_data` and `snapshot_data` keys that points to the data as sent to the server, except for binary data
that is saved to a storage and a path is given instead of the data itself.

### Parsers

The parsers are simple functions that process data from the provided MQ, and post their results. If you wish, you can
add your own parsers, which will be explained at the end of this section.

As an API, you can access it in `BaMMI.parsers` using the `run_parser` method, that, given a parser name and raw data
as published to the MQ, will return the processed result.

As a CLI, the commands `parse` and `run-parser` are available through `python -m cortex.parsers`. While `parse` gets a parser name
and a path to raw data as given from the MQ, process it and returns the results as if they were sent to the MQ,
basically running the parser only once, using `run-parser` with a parser name and a MQ URL (take a look at the server section
for details) will attach the parser to the mQ, consuming raw data, processing and publishing it's result to a dedicated topic in the MQ.

There are 4 parsers provided, processing the user *feelings*, *pose*, *color_image* and *depth_image*.
But what if you want to process a new type of data?
 
 Well that's easy!
 
 All you need to do, is adding a file to _`BaMMI/BaMMI/parsers/all_parsers`_, making sure there's a function named *`parse_*`*
 and that it has a `field` attribute with the name of the field it process from the snapshot data.
 
 ### Saver
 
 The saver is available as `BaMMI.saver`, exposing the `Saver` class, that receives a DB url on it's instantiation, and
 supports the `save` function that given a topic name from the MQ and data in the format that is published to the MQ to this topic, 
 saves the data to the DB.
 
 As with the parsers, the CLI has 2 modes - running `python -m cortex.saver` with the `save` command, that given 
 a DB url (optional with the `-d` or `--database` flags, defaults to `mongodb://BaMMI:1337@mongo:27017`, and follows the URL
 format in the server section), a topic name and a path to data as published to the MQ, will attempt to save it
 to the DB, working only once, or using the `run-saver` command that receives a MQ url and a DB url,
 and consuming anything it can from the MQ and saves it to the DB.
 
 
 ## Future Plans
 
 API (rashly implemented, not yet tested :[ ) and CLI to see the data in the DB, as well as a GUI for easy navigation of all the users data.