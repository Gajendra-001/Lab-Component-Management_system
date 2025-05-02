import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email settings
sender_email = "dhaked1415@gmail.com"
password = "uofo ummg enfd zzcq"
receiver_email = "dhaked1415@gmail.com"

# Create message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email from IoT Lab"

body = "This is a test email to verify your email configuration is working correctly."
message.attach(MIMEText(body, "plain"))

try:
    # Create SMTP session
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    # Login
    server.login(sender_email, password)
    
    # Send email
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Test email sent successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    
finally:
    try:
        server.quit()
    except:
        pass 