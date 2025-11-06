import sys

def calculate_checksum(data_bytes):
    a = 0xFFFF
    words_count = len(data_bytes) // 2
    for i in range(words_count):
        b = data_bytes[2*i] | (data_bytes[2*i + 1] << 8)
        a ^= b
        a = ((a << 1) | (a >> 15)) & 0xFFFF
    return a

def interleave_zeros(arr):
    out = bytearray()
    for b in arr:
        out.append(b)
        out.append(0x00)
    return out

if len(sys.argv) < 2:
    sys.exit(1)

num_str = sys.argv[1].zfill(12)

bcd = bytearray((int(num_str[i]) << 4 | int(num_str[i+1])) for i in range(0, 12, 2))[::-1]
bcd = interleave_zeros(bcd)

chk = calculate_checksum(bcd[::2])
chk_bytes = interleave_zeros(chk.to_bytes(2, "little"))

seq = (bcd + chk_bytes) * 3

footer = interleave_zeros(bytes.fromhex('00FF55AAFF00AF50'))

with open('id.rom', 'wb') as f:
    f.write(seq + footer)