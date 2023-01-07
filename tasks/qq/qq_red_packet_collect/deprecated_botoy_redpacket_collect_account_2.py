# for arm64 version of opqbot

# disable that 复读机 plugin.

# disable this shit. we use the same config.

from base_opq import *


@bot.on_group_msg
def group(ctx: GroupMsg):
    # print('收到群消息，群号为', ctx.FromGroupId)
    data_dict = ctx.data  # recommend to use this json object. or not?
    group_id = data_dict["FromGroupId"]
    RedBaginfo = data_dict["RedBaginfo"]
    if RedBaginfo is not None:
        print("RECEIVED RED PACKET")
        startDaemonThread(openRedBag, (RedBaginfo, group_id))

    # breakpoint()


if __name__ == "__main__":
    bot.run()

# do not send porn shits or you need to relogin.
