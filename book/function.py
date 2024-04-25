from aiogram.types import CallbackQuery
from redis_dict import RedisDict

data = RedisDict()

print(data)
def savat(callback: CallbackQuery, soni, tavar_narxi):
    # product = {}
    # product['soni'] = soni
    # product['tavar_narxi'] = tavar_narxi
    data[str(callback.from_user.id)] = f'''🛒 Savat 

1. IKAR to'plami
{soni} x 259,000 ={tavar_narxi * soni} so'm

Jami: {tavar_narxi * soni} so'm'''
    return data[str(callback.from_user.id)]