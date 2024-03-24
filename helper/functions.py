from users.models import User 
from rest_framework import status
import uuid
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from products.models import CartItem
from django.core.mail import send_mail, EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

#-------------------------- STATUS CODE ---------------------------

status200 = status.HTTP_200_OK
status201 = status.HTTP_201_CREATED
status202 = status.HTTP_202_ACCEPTED
status204 = status.HTTP_204_NO_CONTENT
status400 = status.HTTP_400_BAD_REQUEST
status401 = status.HTTP_401_UNAUTHORIZED
status403 = status.HTTP_403_FORBIDDEN
status404 = status.HTTP_404_NOT_FOUND
status500 = status.HTTP_500_INTERNAL_SERVER_ERROR


#-------------------------------------- CLASS USER FUNCTIONS ------------------------------------

class UserFunctions:
    def get_user(email):
        """
        To get or create user object by mobile number
        params mobile: mobile of user
        result: object
        """
        user_obj = User.objects.get(email=email)
        return user_obj

#-------------------------------------- CLASS RESPONSE HANDLING ------------------------------------

class ResponseHandling:
    def failure_response_message(detail,result):
        """
        error message for failure
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result}

    def success_response_message(detail,result):
        """
        success message for Success
        :param detail: message to show in detail
        :param result : message or result to show
        :returns: dictionary
        """
        return {'detail' : detail, 'result' : result}

#-------------------------------------- ERROR GENERAL FUNCTIONS ------------------------------------

def error_message_function(errors):
    """
    return error message when serializer is not valid
    :param errors: error object
    :returns: string
    """
    for key, values in errors.items():
        error = [value[:] for value in values]
        err = ' '.join(map(str,error))
        return err
    
#-------------------------------------- pdf and email ------------------------------------

def generate_bill_and_send_email(cart_items, recipient_email,user):
    # Generate unique invoice number
    invoice_number = uuid.uuid4().hex[:10].upper()

    # Generate PDF bill
    pdf_file_path = f"invoice_{invoice_number}.pdf"
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    
    # Additional details
    brand_name = "Your Brand Name"
    bill_number = f"Invoice #{invoice_number}"
    user_name = "Name: {}".format(user.name)
    user_email = "Email: {}".format(user.email)
    payment_method = "Payment Method: {}".format("COD")
    
    # Create a style sheet
    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]
    invoice_style = styles["Heading4"]
    user_style = styles["Heading4"]
    
    # Center align the heading
    heading_style.alignment = 1  # 0=left, 1=center, 2=right
    invoice_style.alignment = 0
    user_style.alignment = 0

    # Create a Paragraph for the heading
    heading = Paragraph("Wowman", heading_style)

    bill_number = Paragraph(bill_number, invoice_style)

    user__name = Paragraph(user_name,user_style)
    user__email = Paragraph(user_email,user_style)
    user__payment_method = Paragraph(payment_method,user_style)

    
    table_data = [["Product Name", "Quantity", "Price"]]  # Header row
    
    for item in cart_items:
        product_name = item.product.name
        quantity = item.quantity
        price = item.product.price
        table_data.append([product_name, str(quantity), "Rs."+str(price)])
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    table_data.append(["Total", "", "Rs."+str(total_price)])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build PDF elements
    elements = [heading,user__name,user__email,bill_number,user__payment_method, table]
    doc.build(elements)

    # Send confirmation email with attachment
    email = EmailMessage(
        'Order Confirmation',
        f'Your order (Invoice #{invoice_number}) is confirmed. Please find the attached invoice.',
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
    )
    email.attach_file(pdf_file_path)
    email.send()

    # Delete the temporary PDF file
    os.remove(pdf_file_path)

    return f"Invoice {invoice_number} generated and email sent successfully!"