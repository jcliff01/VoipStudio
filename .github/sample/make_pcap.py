"""Writes a tiny made-up SIP call (INVITE, 180, 200, ACK, RTP both ways, BYE, 200) to call.pcap."""
import sys
from scapy.all import Ether, IP, UDP, Raw, wrpcap

A, B = "192.0.2.10", "198.51.100.20"
cid = "test-call-1@192.0.2.10"
def sip(src, dst, first, cseq, extra=""):
    body = (f"{first}\r\nVia: SIP/2.0/UDP {src}:5060;branch=z9hG4bK{cseq}{len(first)}\r\n"
            f"From: <sip:1001@{A}>;tag=a1\r\nTo: <sip:2002@{B}>" + (";tag=b2" if not first.startswith("INVITE") else "") +
            f"\r\nCall-ID: {cid}\r\nCSeq: {cseq}\r\nContact: <sip:1001@{src}>\r\n{extra}Content-Length: 0\r\n\r\n")
    return Ether(src="02:00:00:00:00:01", dst="02:00:00:00:00:02")/IP(src=src, dst=dst)/UDP(sport=5060, dport=5060)/Raw(body.encode())
def sdp(src, port):
    s = f"v=0\r\no=- 1 1 IN IP4 {src}\r\ns=-\r\nc=IN IP4 {src}\r\nt=0 0\r\nm=audio {port} RTP/AVP 0\r\na=rtpmap:0 PCMU/8000\r\n"
    return s
def sip_sdp(src, dst, first, cseq, port):
    body = sdp(src, port)
    head = (f"{first}\r\nVia: SIP/2.0/UDP {src}:5060;branch=z9hG4bK{cseq}x\r\nFrom: <sip:1001@{A}>;tag=a1\r\n"
            f"To: <sip:2002@{B}>" + (";tag=b2" if not first.startswith("INVITE") else "") +
            f"\r\nCall-ID: {cid}\r\nCSeq: {cseq}\r\nContact: <sip:x@{src}>\r\nContent-Type: application/sdp\r\nContent-Length: {len(body)}\r\n\r\n")
    return Ether(src="02:00:00:00:00:01", dst="02:00:00:00:00:02")/IP(src=src, dst=dst)/UDP(sport=5060, dport=5060)/Raw((head + body).encode())
def rtp(src, dst, sport, dport, seq, ts, ssrc):
    hdr = bytes([0x80, 0]) + seq.to_bytes(2, "big") + ts.to_bytes(4, "big") + ssrc.to_bytes(4, "big")
    return Ether(src="02:00:00:00:00:01", dst="02:00:00:00:00:02")/IP(src=src, dst=dst)/UDP(sport=sport, dport=dport)/Raw(hdr + b"\xff" * 160)
pkts, t = [], 1_700_000_000.0
def add(p, dt):
    global t
    t += dt; p.time = t; pkts.append(p)
add(sip_sdp(A, B, f"INVITE sip:2002@{B} SIP/2.0", "1 INVITE", 20000), 0)
add(sip(B, A, "SIP/2.0 180 Ringing", "1 INVITE"), 0.1)
add(sip_sdp(B, A, "SIP/2.0 200 OK", "1 INVITE", 30000), 2)
add(sip(A, B, f"ACK sip:2002@{B} SIP/2.0", "1 ACK"), 0.05)
for i in range(250):
    add(rtp(A, B, 20000, 30000, i, i * 160, 0x11111111), 0.01)
    add(rtp(B, A, 30000, 20000, i, i * 160, 0x22222222), 0.01)
add(sip(A, B, f"BYE sip:2002@{B} SIP/2.0", "2 BYE"), 0.1)
add(sip(B, A, "SIP/2.0 200 OK", "2 BYE"), 0.05)
wrpcap(sys.argv[1] if len(sys.argv) > 1 else "call.pcap", pkts)
