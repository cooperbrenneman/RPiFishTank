##SSH Connection
Run sshIntoRPi3.ps1 in Powershell as an Administrator.

If you get an error that the script cannot be loaded, run the below code before executing the script again.
Error message:
```"Cannot be loaded because the execution of scripts is disabled on this system."```
Code to run:
```set-executionpolicy remotesigned```