"""Everything the profile says, in one place. Edit here, then run build_static.py."""

LOGIN = "Thulnith-0"
NAME = "Thulnith Perera"

HEADLINE = ("I build software people actually use,", "from desktop tools to ", "AI that speaks Sinhala", ".")
META = ("BSc (Hons) Computer Science", "University of Westminster", "3rd year", "Sri Lanka")

HIGHLIGHTS = [
    ("55.4%", "Sinhala TTS error rate", "(CER), down from 123.1%"),
    ("v3.4.0", "Clamp desktop, shipping", "with auto-updates"),
    ("v1.0.0", "antigravity-delegate", "MCP server, with tests"),
    ("Win + Mac", "AutoTyper, released by", "a GitHub Actions pipeline"),
]

# kind: "public" links to the repo; "private" shows a Private tag and no link.
PROJECTS = [
    {
        "slug": "sinhala-tts",
        "name": "Sinhala TTS",
        "kind": "private",
        "area": "AI · Speech",
        "desc": "Native-accent Sinhala text-to-speech fine-tuned from F5-TTS. It gets the schwa right where "
        "existing Sinhala systems don't. Round-trip CER cut from 123.1% to 55.4%.",
        "tags": [("pytorch", "PyTorch"), (None, "F5-TTS"), ("openai", "Whisper")],
    },
    {
        "slug": "raawa",
        "name": "Raawa · Ahanna v1",
        "kind": "private",
        "area": "AI · Speech",
        "desc": "Sinhala speech-to-text for how people really speak, with the English words they mix in "
        "kept in English. Powers Raawa Studio: on-device Sinhala subtitles for creators.",
        "tags": [("pytorch", "PyTorch"), ("huggingface", "Transformers"), ("vite", "Vite")],
    },
    {
        "slug": "crowdeye",
        "name": "CrowdEye",
        "kind": "private",
        "area": "Computer vision · IoT",
        "desc": "Smart passenger counting for Sri Lankan buses. Computer vision plus sensor fusion "
        "(camera, IR beam, ultrasonic), built for Raspberry Pi / Jetson.",
        "tags": [("python", "Python"), ("opencv", "OpenCV"), (None, "YOLO")],
    },
    {
        "slug": "cri",
        "name": "CRI Plant Request System",
        "kind": "private",
        "area": "Full-stack · Client work",
        "desc": "Internal system for the Coconut Research Institute of Sri Lanka to manage grower "
        "requests for coconut plants. Runs on the office LAN.",
        "tags": [("nextdotjs", "Next.js"), ("typescript", "TypeScript"), ("postgresql", "PostgreSQL"), ("prisma", "Prisma")],
    },
    {
        "slug": "clamp",
        "name": "Clamp",
        "kind": "private",
        "area": "Desktop · Android",
        "desc": "A fast, private video downloader. Desktop app at v3.4.0 with auto-updates, plus an "
        "Android companion. Everything runs on-device, with no account.",
        "tags": [("electron", "Electron"), ("react", "React"), ("capacitor", "Capacitor")],
    },
    {
        "slug": "easy-ai-sub",
        "name": "Easy AI Sub",
        "kind": "public",
        "repo": "Easy-AI-Sub",
        "area": "AI · Desktop",
        "desc": "Offline Windows subtitle generator with GPU/CPU auto-detection. English and Sinhala, "
        "powered by faster-whisper, with a React + Electron UI.",
        "tags": [("python", "Python"), ("openai", "Whisper"), ("electron", "Electron")],
    },
    {
        "slug": "autotyper",
        "name": "AutoTyper",
        "kind": "public",
        "repo": "AutoTyper",
        "area": "Automation · Desktop",
        "desc": "Time-based, human-paced typing automation with an emergency-stop failsafe. Windows and "
        "macOS builds released automatically by GitHub Actions.",
        "tags": [("python", "Python"), (None, "CustomTkinter"), ("githubactions", "Actions")],
    },
    {
        "slug": "antigravity-delegate",
        "name": "antigravity-delegate",
        "kind": "public",
        "repo": "antigravity-delegate",
        "area": "AI agents · MCP",
        "desc": "MCP server that delegates coding and research tasks to Antigravity sub-agents. "
        "Shipped as v1.0.0, with tests.",
        "tags": [("python", "Python"), (None, "FastMCP"), ("pytest", "pytest")],
    },
    {
        "slug": "firestack",
        "name": "FireStack",
        "kind": "private",
        "area": "Desktop · Windows",
        "desc": "Windows optimizer that tunes BlueStacks for Free Fire. Built on .NET 8 with WPF and "
        "an MVVM architecture.",
        "tags": [(None, "C#"), ("dotnet", ".NET 8"), (None, "WPF")],
    },
    {
        "slug": "hydra-panel",
        "name": "Hydra Panel",
        "kind": "private",
        "area": "Desktop · Windows",
        "desc": "C# desktop control panel with license-key sign-in and account registration, built on "
        "a custom Guna UI interface.",
        "tags": [(None, "C#"), (None, "WinForms"), (None, "Guna UI")],
    },
]

STACK = [
    ("Languages", [("python", "Python"), ("typescript", "TypeScript"), ("javascript", "JavaScript"),
                   ("openjdk", "Java"), (None, "C#"), ("dart", "Dart"), ("html5", "HTML"),
                   ("css3", "CSS"), ("postgresql", "SQL")]),
    ("Frontend", [("react", "React"), ("nextdotjs", "Next.js"), ("tailwindcss", "Tailwind CSS"),
                  ("vite", "Vite"), ("framer", "Framer Motion")]),
    ("Apps", [("electron", "Electron"), ("dotnet", ".NET / WPF"), ("python", "CustomTkinter"),
              ("flutter", "Flutter"), ("android", "Android"), ("capacitor", "Capacitor")]),
    ("AI & ML", [("pytorch", "PyTorch"), ("huggingface", "Hugging Face"), ("opencv", "OpenCV"),
                 (None, "YOLO"), ("openai", "Whisper"), (None, "F5-TTS"), ("numpy", "NumPy")]),
    ("Backend", [("postgresql", "PostgreSQL"), ("prisma", "Prisma"), ("firebase", "Firebase"),
                 ("nodedotjs", "Node.js"), (None, "FastMCP")]),
    ("Tooling", [("git", "Git"), ("githubactions", "GitHub Actions"), ("pytest", "pytest"),
                 ("vitest", "Vitest"), ("linux", "Linux")]),
]

SOCIALS = [
    ("github", "GitHub", "Thulnith-0", "https://github.com/Thulnith-0"),
    ("linkedin", "LinkedIn", "thulnith-perera", "https://www.linkedin.com/in/thulnith-perera-42b0bb346"),
    ("instagram", "Instagram", "@thulnith__", "https://www.instagram.com/thulnith__/"),
    ("tiktok", "TikTok", "@_thulnith_", "https://www.tiktok.com/@_thulnith_"),
    ("facebook", "Facebook", "Thulnith Perera", "https://www.facebook.com/share/1F4tUva6wm/"),
    ("discord", "Discord", "Say hi", "https://discord.com/users/922739470837637241"),
    ("gmail", "Email", "thulnithperera870@gmail.com", "mailto:thulnithperera870@gmail.com"),
]
