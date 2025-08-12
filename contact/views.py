from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from .models import ContactMessage

@api_view(['POST'])
def contact_view(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        # Save to database
        contact_message = ContactMessage.objects.create(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            message=serializer.validated_data['message']
        )
        
        # Email content
        subject = f"New Contact Form Submission from {contact_message.name}"
        email_message = f"""
        Name: {contact_message.name}
        Email: {contact_message.email}
        Message: {contact_message.message}
        
        Received at: {contact_message.created_at}
        """
        
        try:
            # Send email
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['bravomzogo@gmail.com'],  # Your email address
                fail_silently=False,
            )
            
            # Also send confirmation to user
            user_subject = "Thank you for contacting Cinetro"
            user_message = f"""
            Dear {contact_message.name},
            
            Thank you for reaching out to us. We have received your message and will get back to you soon.
            
            Your message:
            {contact_message.message}
            
            Best regards,
            The Cinetro Team
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact_message.email],
                fail_silently=False,
            )
            
            return Response(
                {'message': 'Your message has been sent successfully!'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)