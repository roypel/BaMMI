command_prefix="python -m BaMMI.parsers run-parser"
mq_url="rabbitmq://127.0.0.1:5672/"

$command_prefix pose $mq_url & $command_prefix color_image $mq_url & $command_prefix depth_image $mq_url & $command_prefix feelings $mq_url && fg