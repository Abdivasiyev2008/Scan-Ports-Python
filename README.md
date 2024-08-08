# Scan-Ports-Python
You can check all ports of website with this python code ;)

First of all you must install all necessary packages with this command 
> pip install -r req.txt

Next step, if you don't understand how use this code, you should enter this code on terminal
> python main.py --help

Scan ports with default. You can enter IP address. You can replace example.com to any url of website.
> python main.py https://example.com

If you want to start with you entered port. Start [Entered Port] End [65535 Port]
> python main.py --start [port] https://example.com

If you want to add limit
> python main.py --start [start_port] --end [end_port] https://example.com


Created by Sunnatillo
