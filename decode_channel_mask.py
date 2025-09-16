import sys

def mask_to_channels(mask:int):
    chans=[]
    for i in range(0,16):
        if mask & (1<<i):
            chans.append(i)
    return chans

def main():
    if len(sys.argv)<2:
        print("Usage: python decode_channel_mask.py <hex-or-int-mask>")
        return
    s=sys.argv[1]
    if s.lower().startswith('0x'):
        mask=int(s,16)
    else:
        mask=int(s)
    print(f"Mask: 0x{mask:04X} -> channels: {mask_to_channels(mask)}")

if __name__=='__main__':
    main()
