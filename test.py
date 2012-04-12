import sys
import time
from connection import Connection
from userservice import UserService
from vehicleservice import VehicleService
from getpass import getpass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s username (password)" % sys.argv[0]
        exit(2)
    uid = sys.argv[1]

    if len(sys.argv) == 2:
        # Prompt for Password in hidden text
        pwd = getpass("Password: ")
    else:
        pwd = sys.argv[2]

    c = Connection(uid, pwd)
    u = UserService(c)
    print "logging in..."
    d = u.login_and_get_status()
    if not c.logged_in:
        print "Log in invalid, please try again"
    else:
        vin = d.user_info.vin
        print "logged in, vin: %s, nickname: %s" % (vin, d.user_info.nickname)
        v = VehicleService(c)
        print "requesting status..."
        v.request_status(vin)
        print "sleeping for 20 seconds..."
        time.sleep(20)
        print "getting latest..."
        d = u.get_latest_status(vin)
        print "done!"
        import yaml
        print yaml.dump(d)
