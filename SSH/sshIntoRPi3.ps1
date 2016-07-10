#Powershell script to SSH to Raspberry Pi 3

#Lets script executions be enabled on the system
set-executionpolicy remotesigned

#Setting up variables
$DeviceName = "cooper-rpi3-w10"

#Start WinRM service, just in case
net start WinRM

#Add device as trusted host (good to do this in case there are any name/password changes)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value $DeviceName

# Known issue with Powershell that can cause a StackOverflowException on the Powershell client machine. Workaround is to run below command.
remove-module psreadline -ErrorAction SilentlyContinue -force 

# Start session with Raspberry Pi 3
Enter-PSSession -ComputerName $DeviceName -Credential $DeviceName\Administrator