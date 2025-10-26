from typing_extensions import Callable

from patriot.tools.forensics import analyze_forensic_image
from patriot.tools.networking import analyze_packet_tracer_file
from patriot.tools.system import read_text_file, run_shell_command
from patriot.tools.vulnerability import analyze_system_vulnerabilities

TOOLS: list[Callable[..., any]] = [
    analyze_packet_tracer_file,
    analyze_system_vulnerabilities,
    analyze_forensic_image,
    read_text_file,
    run_shell_command,
]
