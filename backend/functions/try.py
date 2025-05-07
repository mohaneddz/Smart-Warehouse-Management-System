import socket
try:
    print(socket.gethostbyname("db.xhdioktfmhlxoezsbair.supabase.co"))
except socket.gaierror as e:
    print(f"DNS resolution failed: {e}")