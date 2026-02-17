# debug_gripper.py
import time
from pymodbus.client import ModbusSerialClient

PORT = "/dev/ttyUSB0"
BAUD = 115200
DEVICE_ID = 9         # laut Manual
POLL_INTERVAL = 0.1   # Sekunden zwischen Polls (100 ms)

def pack_output_registers(rACT, rGTO, rATR, rPR, rSP, rFR):
    """
    Packt die drei 16-bit-Register korrekt gemäß Robotiq-Layout:
      reg_3E8: Byte0=rACT, Byte1=rGTO
      reg_3E9: Byte0=rATR, Byte1=rPR
      reg_3EA: Byte0=rSP,   Byte1=rFR
    """
    reg_3E8 = (rACT & 0xFF) | ((rGTO & 0xFF) << 8)
    reg_3E9 = (rATR & 0xFF) | ((rPR & 0xFF) << 8)
    reg_3EA = (rSP & 0xFF)   | ((rFR & 0xFF) << 8)
    return [reg_3E8, reg_3E9, reg_3EA]

def hex_regs(regs):
    return [hex(r & 0xFFFF) for r in regs]

def read_status(client):
    # Robot Input / Gripper Output first register = 0x07D0 (2000)
    rr = client.read_holding_registers(address=0x07D0, count=2, device_id=DEVICE_ID)
    if rr.isError():
        return None
    # rr.registers is list of two 16-bit values
    return rr.registers

def decode_status(regs):
    # regs[0] = register 0x07D0 (bytes 0/1), regs[1] = 0x07D1 (bytes 2/3)
    # Interpret bytes:
    b0 = regs[0] & 0xFF
    b1 = (regs[0] >> 8) & 0xFF
    b2 = regs[1] & 0xFF
    b3 = (regs[1] >> 8) & 0xFF
    status = {
        "gOBJ (object status byte)": b0,
        "gSTA (gripper status byte)": b1,
        "gFLT (fault byte)": b2,
        "pos_echo (position request echo)": b3
    }
    return status

def read_output_registers(client):
    rr = client.read_holding_registers(address=0x03E8, count=3, device_id=DEVICE_ID)
    if rr.isError():
        return None
    return rr.registers  # list of 3 16-bit registers

def main():
    client = ModbusSerialClient(port=PORT, baudrate=BAUD, parity='N', stopbits=1,
                                bytesize=8, timeout=1)
    if not client.connect():
        print("Fehler: Verbindung zum Modbus-Client fehlgeschlagen.")
        return

    print("Modbus client connected successfully.")

    # --- Saubere Aktivierung: nur rACT setzen, sonst nichts ändern ---
    cur_out = read_output_registers(client)
    if cur_out is None:
        print("Konnte Output-Register nicht lesen. Abbruch.")
        client.close()
        return

    # Zerlege aktuelle Bytes (LowByte, HighByte) für die drei Register
    b0 = cur_out[0] & 0xFF
    b1 = (cur_out[0] >> 8) & 0xFF
    b2 = cur_out[1] & 0xFF
    b3 = (cur_out[1] >> 8) & 0xFF
    b4 = cur_out[2] & 0xFF
    b5 = (cur_out[2] >> 8) & 0xFF
    
    # nur rACT=1 (low byte of reg_3E8) — nutze pack_output_registers, erhalte Rückmeldung
    b0 = 0x1  # rACT
    regs = pack_output_registers(b0, b1, b2, b3, b4, b5)
    print("Aktivierung (nur rACT=1), sende Regs:", hex_regs(regs))
    rr = client.write_registers(address=0x03E8, values=regs, device_id=DEVICE_ID)
    if rr is None or getattr(rr, "isError", lambda: False)():
        print("Fehler beim Schreiben der Aktivierungs-Register:", rr)
        client.close()
        return

    # Warte auf Aktivierung (kleine Schleife, max 3s)
    t0 = time.time()
    while time.time() - t0 < 3.0:
        s = read_status(client)
        if s:
            dec = decode_status(s)
            # Optional: prüfe ein Status-Flag das Aktivierung anzeigt; hier als Beispiel pos_echo != 0
            if dec["gSTA (gripper status byte)"] != 0:
                print("Aktiviert:", hex_regs(s), decode_status(s))
                break
        time.sleep(0.1)

    # Read status once
    s = read_status(client)
    if s:
        print("Status nach Aktivierung:", hex_regs(s), decode_status(s))
    else:
        print("Konnte Status nicht lesen (nach Aktivierung).")


    # --- Nun rPR + rGTO setzen (Bewegung auslösen) ---
    target_position = 100  # 0..255
    cur_out = read_output_registers(client)
    if cur_out is None:
        print("Konnte Output-Register nicht lesen vor GoTo. Abbruch.")
        client.close()
        return

    b0 = cur_out[0] & 0xFF
    b1 = (cur_out[0] >> 8) & 0xFF
    b2 = cur_out[1] & 0xFF
    # setze neues PR in HighByte der 2. Register and only set rGTO bit (preserve other bits)
    b3 = target_position  # rPR -> high byte of reg_3E9
    b1 = b1 | 0x01        # rGTO: nur Bit 0 setzen, andere Bits erhalten
    # SP/FR explizit setzen (oder belassen)
    b4 = 255  # speed byte
    b5 = 255  # force byte

    regs = pack_output_registers(b0, b1, b2, b3, b4, b5)
    print("Sende GoTo (rGTO=1), Position:", target_position, "Regs:", hex_regs(regs))
    rr = client.write_registers(address=0x03E8, values=regs, device_id=DEVICE_ID)
    if rr is None or getattr(rr, "isError", lambda: False)():
        print("Fehler beim Schreiben der GoTo-Register:", rr)
        client.close()
        return
    s = read_status(client)
    if s:
        print("Status nach ??:", hex_regs(s), decode_status(s))
    else:
        print("Konnte Status nicht lesen (nach Aktivierung).")

    # Polling wie gehabt...
    timeout = 5.0
    t0 = time.time()
    while time.time() - t0 < timeout:
        s = read_status(client)
        if not s:
            print("Fehler beim Lesen der Statusregister.")
            break
        decoded = decode_status(s)
        print("Status:", hex_regs(s), decoded)
        # pos_echo liefert meist die aktuelle position echo im Byte3
        pos_echo = decoded["pos_echo (position request echo)"]
        gflt = decoded["gFLT (fault byte)"]
        gsta = decoded["gSTA (gripper status byte)"]
        # Typische Check-Bedingungen:
        if gflt != 0:
            print("Fehler im Greifer (gFLT != 0):", hex(gflt))
            break
        # Prüfe ob pos_echo == target_position oder gSTA zeigt 'stopped'
        if pos_echo == target_position:
            print("Position erreicht (pos_echo == target).")
            break
        time.sleep(POLL_INTERVAL)

    client.close()
    print("Fertig.")

if __name__ == "__main__":
    main()
