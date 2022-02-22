import boto3
from botocore.exceptions import ClientError

class EmailSender:
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    # SENDER = "wjtay1998@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    # RECIPIENT = "wjtay1998@gmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-southeast-1"

    # The character encoding for the email.
    CHARSET = "UTF-8"

    def __init__(self) -> None:
        pass

    def send_email(self, sender, recipient, subject, body_text, body_html):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body_text = body_text
        self.body_html = body_html

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',
            region_name=self.AWS_REGION,
            aws_access_key_id="AKIASQTSZB4HBAJU4Y3O",
            aws_secret_access_key="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",)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        self.recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': self.body_html,
                        },
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': self.body_text,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': self.subject,
                    },
                },
                Source=self.sender,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
