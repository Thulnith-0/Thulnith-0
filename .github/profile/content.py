"""Everything the profile says, in one place. Edit here, then run build_static.py."""

LOGIN = "Thulnith-0"
NAME = "Thulnith Perera"

HEADLINE = ("I build software people actually use,", "from desktop tools to ", "intelligent systems", ".")
META = ("BSc (Hons) Computer Science", "University of Westminster", "3rd year", "Sri Lanka")


# kind: "public" links to the repo; "private" shows a Private tag and no link.
PROJECTS = [
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
                 (None, "YOLO"), ("openai", "Whisper"), ("numpy", "NumPy")]),
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
    ("facebook", "Facebook", "Thulnith Perera", "https://www.facebook.com/thulnith.perera.98/"),
    ("discord", "Discord", "Say hi", "https://discord.com/users/922739470837637241"),
    ("gmail", "Email", "thulnithperera870@gmail.com", "mailto:thulnithperera870@gmail.com"),
]


# Terminal "about me": (command, output) pairs, typed out in order.
TERMINAL = [
    ("whoami", "Thulnith Perera · CS undergrad, University of Westminster · Sri Lanka"),
    ("cat focus.txt", "AI  ·  desktop apps  ·  computer vision"),
    ("ls ~/shipped", "AutoTyper   Easy-AI-Sub   antigravity-delegate   Clamp"),
    ("echo $MOTTO", "Learn fast. Build hard. Improve constantly."),
]

# Journey timeline: (month the repo was started, title). Dates from the GitHub API.
JOURNEY = [
    ("Nov 2024", "Joined GitHub"),
    ("Jun 2025", "CrowdEye"),
    ("Mar 2026", "AutoTyper"),
    ("May 2026", "Easy AI Sub"),
    ("Jun 2026", "Clamp"),
    ("Aug 2026", "antigravity-delegate"),
    ("Nov 2026", "CRI system"),
]

# Display names for repos in the activity cards. Repos that share a name are grouped
# (all Mint repos show as one "Mint" row in "Contributed to"); any repo not listed here
# is shown under its own name. Private repos are private to hide their code only:
# their activity (names, commit counts) is always shown.
REPO_NAMES = {
    "autotyper": "AutoTyper",
    "easy-ai-sub": "Easy AI Sub",
    "antigravity-delegate": "antigravity-delegate",
    "crowdeye": "CrowdEye",
    "crowdeye-iot-console": "CrowdEye",
    "crowdeye-website": "CrowdEye",
    "crowdeye-marketing-website": "CrowdEye",
    "cri-plant-distribution-system": "CRI Plant Request System",
    "clamp_pc": "Clamp",
    "clamp_mobile": "Clamp",
    "firestack": "FireStack",
    "hydra-panel-0.2": "Hydra Panel",
    "thulnith-0": "This profile",
    "mint": "Mint",
    "mint_android": "Mint",
    "mint_mobile": "Mint",
    "mint-downloader": "Mint",
    "mint-webhook-server": "Mint",
    "mint_email_engine": "Mint",
    "mint_the_aggregator": "Mint",
    "database_system_and_the_mint_harvester": "Mint",
}

# Commit authors counted as the profile owner's own work, besides the owner's account:
# commits made by Claude in Claude Code sessions.
EXTRA_AUTHOR_EMAILS = {"noreply@anthropic.com"}

# Never shown anywhere: student IDs. Some coursework repo names contain them
# (e.g. w2120618-20232673-CSA-CW), so they're stripped from displayed names.
STUDENT_ID_PATTERNS = [r"w\d{7}", r"\d{8}"]

# Repos whose names stay off the profile (owner's choice). Their commits still count, as
# a total. Stored as the first 16 hex chars of sha256(lowercase repo name), so the names
# aren't readable in this public repo. To add one:
#   python -c "import hashlib;print(hashlib.sha256(b'repo-name').hexdigest()[:16])"
HIDDEN_REPO_HASHES = {
    "21262a3cb5337627",
    "4284445d08ba5d6b",
    "472e62a0e69e00bb",
    "84dd92e71bf11162",
    "8662804e6d830708",
    "aade094721c39737",
    "b437457fc5c466e7",
    "d5b0ea00e403fd3b",
    "f243d99b7853fc5b",
}
