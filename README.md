# VoipStudio

**Project credit:** A coworker of mine came up with the original idea for this project.

Windows desktop and command-line tools for inspecting VoIP signaling in packet captures. This repository contains the packaged binaries, [build information](build-info.txt), and [user manual](VoipStudio-Manual.html).

## Run on Windows

1. Install the .NET 10 Desktop Runtime for Windows x64.
2. Download and extract the repository ZIP. Keep the EXEs and DLLs together.
3. Run `VoipStudio.exe` for the desktop application, or run `vsx.exe --help` from the extracted folder for command-line options.

Playback of iLBC, G.723.1, and AMR requires FFmpeg. Put FFmpeg on PATH or in an `ffmpeg` folder beside `VoipStudio.exe`. Open the manual in a browser for usage instructions.

Packet captures can contain phone numbers, network addresses, or call audio. Use sanitized captures when sharing examples.

## License

This binary distribution has no published redistribution license. Confirm reuse terms with the maintainer. Separately installed components have their own terms.
