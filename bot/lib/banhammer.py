import datetime
import math


from ..locale import locale
from .text import prettyword



def ban(blocker_message,
        blockable_message,
        time,
        reason = "Причина не указана"
        ):
    
    try:
        ban_time = math.ceil(float(time))
    except ValueError:
        bt = datetime.time.fromisoformat(time)
        ban_time = bt.hour + bt.minute

    until_date = datetime.datetime.now() + datetime.timedelta(minutes = ban_time)
    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=until_date.timestamp())

    time_localed=prettyword(ban_time, locale.minutes),
    unban_time=until_date.isoformat()
    
    ban_log = locale.ban_template.format(
        name=blockable_message.from_user.full_name,
        banchik=blocker_message.from_user.full_name,
        userid=blockable_message.from_user.id,
        why=reason,
        time=time,
        time_localed=time_localed,
        unban_time=unban_time
    )


    if message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")

    try:
        await message.delete()
        await bot.send_message(message.chat.id, ban_log,
                               reply_to_message_id=reply.message_id,
                               parse_mode="HTML")
    except Exception:
        await message.reply(ban_log, parse_mode="HTML")



def __calc_ban_time(time):
    if time == 0:
        return "никогда))"

    ts = datetime.now(TIMEZONE).timestamp() + time * 60
    return TIMEZONE.localize(datetime.fromtimestamp(ts))