#
# (c) 2025 Yoichi Tanibayashi
#
import time

import click
import pigpio

from ..core.piservo import PiServo
from ninja_utils.my_logger import get_logger


class CmdServo:
    """servo command"""

    def __init__(self, pi, pin, pulse, sec=1.0, debug=False):
        self._debug = debug
        self.__log = get_logger(__class__.__name__, self._debug)
        self.__log.debug('pin=%s, pulse="%s", sec=%s', pin, pulse, sec)

        self.pin = pin
        self.pulse_str = pulse
        self.sec = sec

        self.pi = pi
        if not self.pi.connected:
            self.__log.error("pigpio daemon not connected.")
            raise ConnectionError("pigpio daemon not connected.")

        self.servo = PiServo(self.pi, self.pin, debug=self._debug)

    def main(self):
        """main"""
        try:
            pulse_int = int(self.pulse_str)
        except ValueError:
            if self.pulse_str == "min":
                pulse_int = PiServo.MIN
            elif self.pulse_str == "max":
                pulse_int = PiServo.MAX
            elif self.pulse_str == "center":
                pulse_int = PiServo.CENTER
            else:
                self.__log.warning(
                    '"%s": invalid pulse string', self.pulse_str
                )
                pulse_int = -1

            self.__log.debug("pulse_int=%s", pulse_int)

        if PiServo.MIN <= pulse_int <= PiServo.MAX:
            self.servo.move_pulse(pulse_int)
            print(f"pin={self.pin}, pulse={pulse_int}")
            time.sleep(self.sec)
        else:
            self.__log.error(
                "pulse_int=%s: invalid value. do nothing", pulse_int
            )

    def end(self):
        """end"""
        self.__log.debug("")
        self.servo.off()
        print("done")


@click.command()
@click.argument("pin", type=int)
@click.argument("pulse", type=str)
@click.option("--sec", "-s", "sec", type=float, default=1.0, help="sleep time")
@click.option("--debug", "-d", "debug", is_flag=True, help="debug flag")
def main(pin, pulse, sec, debug):
    """
    Move servo to <PULSE>
    
    PULSE: min | center | max | <pulse_width>
    """
    log = get_logger(__name__, debug)

    pi = pigpio.pi()

    try:
        app = CmdServo(pi, pin, pulse, sec, debug=debug)
        app.main()
    except Exception as e:
        log.error(e)
    finally:
        app.end()
        log.debug("finally")


if __name__ == "__main__":
    main()
