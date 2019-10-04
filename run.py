from app import app, db
from subprocess import check_output
from zeroconf import ServiceInfo, Zeroconf
import socket
import sys

if __name__ == '__main__':
    # REGISTER ZEROCONF SERVICE
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if '-pi' in sys.argv:
        IPAddr = str(check_output(['hostname', '-I']), 'utf-8')
    desc = {'version': '1.0'}
    info = ServiceInfo("_http._tcp.local.",
    "Attendance System._http._tcp.local.",
    socket.inet_aton(IPAddr), 80, 0, 0,
    desc, "attendancesys.local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    # RUN APPLICATION
    app.run(host='0.0.0.0', debug=True)
