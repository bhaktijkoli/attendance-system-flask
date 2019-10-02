from app import app, db
import socket
from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':
    # REGISTER ZEROCONF SERVICE
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    desc = {'path': '/~paulsm/'}
    info = ServiceInfo("_http._tcp.local.",
    "Attendance System._http._tcp.local.",
    socket.inet_aton(IPAddr), 80, 0, 0,
    desc, "attendancesys.local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    # RUN APPLICATION
    app.run(host='0.0.0.0', debug=True)
