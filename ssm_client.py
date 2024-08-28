import boto3
import time

# Initialize a session using Amazon SSM
ssm_client = boto3.client('ssm')

# Define the instance ID and the file path to delete
instance_id = 'i-0abcd1234efgh5678'  # Replace with your instance ID
file_path = '/path/to/your/file.txt'  # Replace with the path to the file you want to delete

# Define the shell script to check if the file exists and delete it if it does
command = f'''
if [ -f "{file_path}" ]; then
    rm -f "{file_path}"
    echo "File deleted"
else
    echo "File does not exist"
fi
'''

# Send the command to the instance
response = ssm_client.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [command]}
)

# Print the command ID to track the execution
command_id = response['Command']['CommandId']
print(f'Command ID: {command_id}')

# Function to check the status of the command
def check_command_status(command_id, instance_id):
    while True:
        response = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )
        status = response['Status']
        print(f'Command status: {status}')
        if status in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
            print(f'Command output: {response["StandardOutputContent"]}')
            print(f'Command error: {response["StandardErrorContent"]}')
            break
        time.sleep(5)  # Wait for 5 seconds before checking again

# Check the status of the command
check_command_status(command_id, instance_id)
