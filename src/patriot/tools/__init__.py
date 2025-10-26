from typing_extensions import Callable
from patriot.tools.networking import analyze_packet_tracer_file
from patriot.tools.vulnerability import analyze_system_vulnerabilities
from patriot.tools.forensics import analyze_forensic_image

TOOLS: list[Callable[..., any]] = [
    analyze_packet_tracer_file,
    analyze_system_vulnerabilities,
    analyze_forensic_image,
]
