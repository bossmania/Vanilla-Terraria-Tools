import envs
import logger

def control_output(line, proc):
    #timestamp the stdout line and print it
    stamped = logger.timestamp(line)
    print(stamped)

    #organize the messages for logging
    organize_log_messages(line, stamped, proc)


def organize_log_messages(line, stamped, proc):
    #log the player's IP
    if envs.IP_regex.search(line):
        logger.write_player(line)

    #log the chat message
    elif envs.chat_regex.search(line):
        #log the chat message
        logger.write_log(stamped, envs.CHAT_LOG)

    #log everything else
    else:
        logger.write_log(stamped, envs.OTHER_LOG)
