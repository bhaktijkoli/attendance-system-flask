from app import app, db
import socket
from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':
    # REGISTER ZEROCONF SERVICE
    desc = {'path': '/~paulsm/'}
    info = ServiceInfo("_http._tcp.local.",
    "Attendance System._http._tcp.local.",
    socket.inet_aton("127.0.0.1"), 80, 0, 0,
    desc, "attendancesys.local.")

    zeroconf = Zeroconf()
    zeroconf.register_service(info)

    # RUN APPLICATION
    app.run(host='0.0.0.0', debug=True)
