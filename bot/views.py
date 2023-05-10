
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse=WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt    
def callback(request):
    words=['早安!您好','天氣很不錯','祝您上班順利','吃飽睡飽才有精神','要帶傘','再說一次?','你要跟詠竣抱抱']
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')
        try:
            events=parse.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event,MessageEvent):
                if isinstance(event.message,TextMessage):
                    text=event.message.text
                    print(text)
                    if '電影' in text:
                        message= 'https://movies.yahoo.com.tw/'
                    elif '捷運' in text:
                        message= 'https://tw.piliapp.com/mrt-taiwan/taipei/'
                    elif '樂透' in text :
                        message = lotto()
                    elif '早安' in text :
                        message = random.choice(words)
                    else:
                        message = text
                    
    
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=message)
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='無法解析')
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
def lotto():
    numbers = sorted(random.sample(range(1,50),6))
    result = ' '.join(map(str, numbers))

    return (f'本期樂透號碼為:{result}')

