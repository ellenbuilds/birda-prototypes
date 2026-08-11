#!/usr/bin/env python3
"""Bake a white sticker border into a keyed bird cutout.

The border used to be a CSS drop-shadow chain, which is either blurry (blurred
shadows) or lumpy (zero-blur shadows thick enough to match the supplied robin
card art). Baking it gives a uniform edge at no runtime cost — which matters,
since these cards flip and sway.

Grows the canvas by R, dilates the alpha mask by R as an octagon (alternating
4- and 8-neighbour passes approximate a disc), and fills white behind it.
R is in SOURCE pixels; on the collection card a 460-wide cutout is fitted into
a 202px box, so the rendered border is R * 202 / (460 + 2R).
"""
import struct, zlib, sys, os

def read_png(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n'
    pos, idat = 8, bytearray()
    w = h = ct = None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]
        typ = d[pos+4:pos+8]; data = d[pos+8:pos+8+ln]
        if typ == b'IHDR':
            w, h, bd, ct, _, _, il = struct.unpack('>IIBBBBB', data)
            assert bd == 8 and il == 0 and ct == 6, 'expected 8-bit RGBA'
        elif typ == b'IDAT': idat += data
        elif typ == b'IEND': break
        pos += 12 + ln
    raw = zlib.decompress(bytes(idat)); stride = w*4
    out = bytearray(stride*h); prev = bytearray(stride); p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p+stride]); p += stride
        if f == 1:
            for i in range(4, stride): line[i] = (line[i]+line[i-4]) & 255
        elif f == 2:
            for i in range(stride): line[i] = (line[i]+prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i-4] if i >= 4 else 0
                line[i] = (line[i] + ((a+prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i-4] if i >= 4 else 0; b = prev[i]
                c = prev[i-4] if i >= 4 else 0
                pp = a+b-c; pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i]+pr) & 255
        out[y*stride:(y+1)*stride] = line; prev = line
    return w, h, out

def write_png(path, w, h, rgba):
    raw = bytearray(); stride = w*4
    for y in range(h):
        raw.append(0); raw += rgba[y*stride:(y+1)*stride]
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t+d) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)

def trim(w0, h0, px0, thresh=128):
    """Crop to the opaque content, so every bird is framed the same way — the
    keyed photos keep their original margins, which made each one land at a
    different size inside the card's art box.

    The threshold matters: some cutouts carry a faint wash of near-transparent
    pixels right across the frame (the keyer's ramp over a noisy background), so
    trimming on `alpha > 8` finds no margin at all. The robin measured its full
    460x345 canvas that way; at 128 it is 323x329, which is the bird."""
    x0, y0, x1, y1 = w0, h0, -1, -1
    for y in range(h0):
        row = y*w0*4
        for x in range(w0):
            if px0[row + x*4 + 3] > thresh:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    cw, ch = x1-x0+1, y1-y0+1
    out = bytearray(cw*ch*4)
    for y in range(ch):
        s = ((y+y0)*w0 + x0)*4; t = y*cw*4
        out[t:t+cw*4] = px0[s:s+cw*4]
    return cw, ch, out

def border(src, dst, target_css, box=202):
    w0, h0, px0 = read_png(src)
    w0, h0, px0 = trim(w0, h0, px0)
    # R such that the border renders at target_css once the art is fitted to the
    # box: target = R * box / (long + 2R)
    long_side = max(w0, h0)
    R = max(1, round(target_css * long_side / (box - 2*target_css)))
    w, h = w0 + 2*R, h0 + 2*R
    px = bytearray(b'\xff\xff\xff\x00' * (w*h))
    for y in range(h0):
        s = y*w0*4; t = ((y+R)*w + R)*4
        px[t:t+w0*4] = px0[s:s+w0*4]
    mask = bytearray(w*h)
    for i in range(w*h):
        if px[i*4+3] > 128: mask[i] = 1
    # octagon dilation: alternate cross and full 3x3 passes
    for step in range(R):
        nxt = bytearray(mask)
        diag = (step % 2 == 1)
        for y in range(1, h-1):
            row = y*w
            for x in range(1, w-1):
                if mask[row+x]: continue
                if (mask[row+x-1] or mask[row+x+1] or mask[row-w+x] or mask[row+w+x]
                    or (diag and (mask[row-w+x-1] or mask[row-w+x+1]
                                  or mask[row+w+x-1] or mask[row+w+x+1]))):
                    nxt[row+x] = 1
        mask = nxt
    added = 0
    for i in range(w*h):
        if mask[i] and px[i*4+3] < 255:
            a = px[i*4+3]
            if a == 0:
                px[i*4:i*4+4] = b'\xff\xff\xff\xff'; added += 1
            else:
                # keep the cutout's own soft edge over solid white
                px[i*4:i*4+3] = bytes(( (px[i*4+j]*a + 255*(255-a))//255 for j in range(3) ))
                px[i*4+3] = 255
    write_png(dst, w, h, bytes(px))
    return w0, h0, w, h, R, R*box/(max(w0,h0)+2*R)

if __name__ == '__main__':
    target = float(sys.argv[1]); src_dir, dst_dir = sys.argv[2], sys.argv[3]
    for f in sorted(os.listdir(src_dir)):
        if not f.endswith('.png'): continue
        w0, h0, w, h, R, css = border(os.path.join(src_dir, f), os.path.join(dst_dir, f), target)
        print('%-18s trimmed %dx%d → %dx%d   R=%d → %.1f CSS px   %d KB'
              % (f, w0, h0, w, h, R, css, os.path.getsize(os.path.join(dst_dir, f))//1024))
