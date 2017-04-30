# Import required Python libraries
import os
import RPi.GPIO as GPIO
import time
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage
camera = picamera.PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4

print 'PIR Module Test (CTRL-C to exit)'

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)
Current_State  = 0
Previous_State = 0

try:

  print 'Waiting for PIR to settle ...'

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0

  print '  Ready'

  # Loop until users quits with CTRL-C
  while True :

    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)

    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print '  Motion detected'
      tempImgName = str(time.time()) + '.jpg'
      tempImgPath = 'imgMail/image-' + tempImgName
      camera.vflip = True
      camera.capture(tempImgPath)

      # Send the message via an SMTP server

      img_data = open(tempImgPath, 'rb').read()
      msg = MIMEMultipart()
      msg['Subject'] = 'Movement Detected'
      msg['From'] = 'sending.account@gmail.com'
      msg['To'] = 'receiving.account.com'
      text = MIMEText('Something is happening!')
      msg.attach(text)
      image = MIMEImage(img_data, name=os.path.basename(tempImgName))
      msg.attach(image)
      print '  Sending email'
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.ehlo()
      s.starttls()
      s.ehlo()
      s.login('sending.account@gmail.com', 'password')
      s.sendmail('sending.account@gmail.com', 'receiving.account.com', msg.as_string())
      s.quit()
      print '  Mail sent'
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      # os.remove(tempImgPath)
      print '  Ready'
      Previous_State=0

    # Wait for 10 milliseconds
    time.sleep(0.01)

except KeyboardInterrupt:
  print '  Quit'
  # Reset GPIO settings
  GPIO.cleanup()
