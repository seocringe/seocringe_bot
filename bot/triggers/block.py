from ..config import dp #importing the config variable 
from aiogram import types #importing the types module from aiogram library 

@dp.message_handler(lambda x: x.forward_from_chat #checking the condition of forward messages 
and x.chat.id in [-1001176998310] #filtering the messages been received from the specific chat 
and ( #checking the condition 
        ( #nested checking 
            x.from_user.id in [675257916, 811510365]
            and x.forward_from_chat.id in [-1001113237212]
        )
        or (x.forward_from_chat.id in [-1001204336102]) #list of chats to filter messages from 
        or ( #nested checking 
            x.from_user.id in [
                # 1890967276, #list of users IDs 
                # 679350651,
            ]
            and x.forward_from_chat.id < 0 #messages with chat ID less than 0
        )
    ),
    content_types=types.ContentType.ANY, #allowing any content type to filter
)
async def just_blocker(message: types.Message): #defining the function 
    await message.delete() #deleting the filtered messages