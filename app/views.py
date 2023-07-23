from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client


class SendSMSView(APIView):
    def post(self, request, format=None):
        account_sid = ''
        auth_token = ''
        from_number = '' # Twilio tomonidan berilgan raqam
        to_number = request.data.get('to_number', None) # POST so'rovdan kelgan raqam
        message = request.data.get('message', None) # POST so'rovdan kelgan xabar

        if not to_number or not message:
            return Response(
                {'error': 'to_number va message bo\'sh bo\'lishi mumkin emas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        client = Client(account_sid, auth_token)

        try:
            message = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            return Response(
                {'success': 'Xabar yuborildi.', 'message_id': message.sid},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
