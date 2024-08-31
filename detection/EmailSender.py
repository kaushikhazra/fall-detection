import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailSender:
    '''
    Class responsible for sending email
    '''

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password, recipient_email):
        '''
        Constructor that is responsible 
        for initializing the email client
        '''
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def send_email(self, image_path):
        '''
        Sends the email
        '''

        # The sender, receiver, subject 
        # and body configuration
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = '!!URGENT!FALL AT CAM1 LOCATION !!'

        image_cid = 'image1'
        html_body = f"""
        <html>
        <body>
            <p>Dear User,</p>
            <p>Incident detected at CAM1 that needs your ATTENTION!</p>
            <img src="cid:{image_cid}" alt="Clickable Image" style="width:300px;height:auto;">
            <p>
            <a href="https://www.example.com">
                Click here to see the video
            </a>
            </p>
            <p>
            Thank you,<br/>
            Fall Detection System
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Attach the image of the fall
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read(), name='image.jpg')
            img.add_header('Content-ID', f'<{image_cid}>')
            msg.attach(img)

        # Send email
        try:
            print('Sending Email')
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            text = msg.as_string()
            server.sendmail(self.sender_email, self.recipient_email, text)

            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email: {e}')
        finally:
            server.quit()