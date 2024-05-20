all:
	pyinstaller client.py --onefile --noconsole --specpath bin/client --distpath bin/client &
	pyinstaller server.py --onefile --specpath bin/server --distpath bin/server