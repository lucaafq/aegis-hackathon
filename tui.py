import time
import psutil
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Label, Static
from textual.containers import Horizontal, Vertical, VerticalScroll
from agent import ask_agent

class SystemMonitor(Static):
    """Monitorizeaza utilizarea reala a sistemului pe MacBook M1."""
    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_stats)
        
    def generate_bar(self, percentage: float, width: int = 15) -> str:
        filled = int((percentage / 100.0) * width)
        return "■" * filled + "□" * (width - filled)

    def update_stats(self) -> None:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        content = (
            f"[bold #94a3b8]CPU USE:[/bold #94a3b8]  [{self.generate_bar(cpu)}] [italic]{cpu}%[/]\n"
            f"[bold #94a3b8]RAM USE:[/bold #94a3b8]  [{self.generate_bar(ram)}] [italic]{ram}%[/]"
        )
        self.update(content)

class AegisTerminal(App):
    CSS = """
    Screen {
        background: #020617;
    }
    Header {
        background: #0f172a;
        color: #38bdf8;
        border-bottom: solid #1e293b;
        text-style: bold;
    }
    Footer {
        background: #0f172a;
        color: #475569;
    }
    #main_layout {
        height: 100%;
    }
    /* Sidebar Styling */
    #sidebar {
        width: 45;
        dock: left;
        padding: 1 2;
        border-right: vkey #1e293b;
        background: #020617;
    }
    .panel_title {
        background: #1e293b;
        color: #f8fafc;
        padding: 0 1;
        margin-top: 1;
        margin-bottom: 1;
        text-style: bold;
    }
    .sys_label {
        color: #64748b;
    }
    .sys_value {
        color: #38bdf8;
        text-style: italic;
    }
    .alert_value {
        color: #4ade80;
        text-style: bold italic;
    }
    .author_badge {
        color: #475569;
        margin-top: 2;
        text-align: center;
        text-style: bold;
    }
    /* Main Chat Area */
    #chat_area {
        width: 100%;
        height: 100%;
    }
    #chat_log {
        padding: 1 3;
        background: #020617;
        color: #cbd5e1;
        border: blank;
        height: 1fr;
    }
    /* Input Box Styling */
    #input_container {
        height: auto;
        border-top: solid #1e293b;
        background: #0f172a;
        padding: 1;
    }
    Input {
        background: #020617;
        color: #38bdf8;
        border: round #334155;
        width: 100%;
    }
    Input:focus {
        border: double #38bdf8;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal(id="main_layout"):
            with VerticalScroll(id="sidebar"):
                yield Label("+ ARCHITECTURE", classes="panel_title")
                yield Label("LLM Engine:", classes="sys_label")
                yield Label("  Google Gemini API [v3.5]", classes="sys_value")
                yield Label("Crypto Engine:", classes="sys_label")
                yield Label("  Native C-Shared (.dylib)", classes="sys_value")
                yield Label("Integration:", classes="sys_label")
                yield Label("  Low-Level FFI (ctypes)", classes="sys_value")
                
                yield Label("+ SECURITY PROTOCOL", classes="panel_title")
                yield Label("Model: Zero-Trust Proxy", classes="sys_label")
                yield Label("Master Key: Air-Gapped", classes="sys_label")
                yield Label("Intercept Status: ACTIVE", classes="alert_value")
                
                yield Label("+ SYSTEM TELEMETRY", classes="panel_title")
                yield SystemMonitor()
                
                yield Label("MADE BY LUCAAFQ", classes="author_badge")

            with Vertical(id="chat_area"):
                yield RichLog(id="chat_log", wrap=True, markup=True)
                
                with Vertical(id="input_container"):
                    yield Input(
                        placeholder="root@aegis:~# Inject prompt (use [brackets] for local encryption)...", 
                        id="prompt"
                    )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "AEGIS SECURE PROXY // ENTERPRISE TERMINAL"
        log = self.query_one(RichLog)
        log.write("[bold #4ade80]OK -[/bold #4ade80] [italic]Boot sequence initiated...[/]")
        log.write("[bold #4ade80]OK -[/bold #4ade80] [italic]Memory pointers to C-engine allocated.[/]")
        log.write("[bold #4ade80]OK -[/bold #4ade80] [italic]Host LLM API endpoint verified.[/]")
        log.write("\n[bold #94a3b8]* System ready. Awaiting secure prompt injection.[/]\n")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        log = self.query_one(RichLog)
        user_text = event.value
        self.query_one(Input).value = ""
        
        if not user_text.strip():
            return

        log.write(f"\n[bold #38bdf8]root@aegis:~#[/bold #38bdf8] [bold white]{user_text}[/]")
        log.write("[italic #64748b]* Processing local encryption algorithms...[/]")
        
        try:
            start_time = time.time()
            
            # Executam scripturile backend
            safe_prompt, llm_response = ask_agent(user_text)
            
            latency_ms = round((time.time() - start_time) * 1000, 2)
            
            # Afisam payload-ul care pleaca pe retea
            log.write(f"[bold #f87171]INTERCEPT:[/bold #f87171] [italic]Sanitized payload broadcasted:[/italic] {safe_prompt}")
            
            # Raspunsul AI-ului + Latenta calculata real
            log.write(f"\n[bold #4ade80]AEGIS AI RESPONSE[/bold #4ade80] [italic #64748b](Latency: {latency_ms}ms)[/]")
            log.write(f"[#f8fafc]{llm_response}[/]\n")
            log.write("[#1e293b]" + "━" * 60 + "[/]")
            
        except Exception as e:
            log.write(f"[bold red]FATAL EXCEPTION:[/bold red] [italic]{str(e)}[/]")

if __name__ == "__main__":
    app = AegisTerminal()
    app.run()