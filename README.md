<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Next-Gen GitHub Dashboard</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        void: '#09090B',
                        frost: '#18181B',
                        cyan: '#00E5FF',
                        matrix: '#00FF41',
                        purple: '#B026FF',
                        muted: '#A1A1AA'
                    },
                    animation: {
                        'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'flicker': 'flicker 0.15s ease-in-out 2',
                    },
                    keyframes: {
                        flicker: {
                            '0%, 100%': { opacity: '1' },
                            '50%': { opacity: '0.5' },
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #09090B; color: #FAFAFA; }
        .glass-panel {
            background: rgba(24, 24, 27, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .neon-border-cyan:hover {
            border-color: #00E5FF;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
        }
        .neon-border-purple:hover {
            border-color: #B026FF;
            box-shadow: 0 0 15px rgba(176, 38, 255, 0.3);
        }
        
        /* 3D Heatmap Block Styles */
        .heatmap-block {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            transition: all 0.2s ease;
            cursor: pointer;
            box-shadow: inset 1px 1px 2px rgba(255,255,255,0.1), inset -1px -1px 2px rgba(0,0,0,0.5);
        }
        .heatmap-block:hover {
            transform: translateY(-3px) scale(1.1);
            box-shadow: 0 5px 10px rgba(0,0,0,0.5), inset 1px 1px 2px rgba(255,255,255,0.3);
            z-index: 10;
        }
        
        /* Level Progress Bar */
        progress::-webkit-progress-bar { background-color: #27272A; border-radius: 999px; }
        progress::-webkit-progress-value { background-color: #B026FF; border-radius: 999px; box-shadow: 0 0 10px rgba(176, 38, 255, 0.5); }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 selection:bg-cyan selection:text-void flex flex-col gap-6" id="app-body">

    <!-- 1. The Command Center (Sticky Header) -->
    <header class="sticky top-0 z-50 glass-panel rounded-xl p-4 flex items-center justify-between shadow-2xl transition-all duration-200" id="cmd-center">
        <div class="flex items-center gap-3">
            <i data-lucide="terminal" class="text-cyan"></i>
            <span class="font-bold text-lg tracking-wider hidden md:block">NEXUS_HUB</span>
        </div>
        
        <div class="flex-1 max-w-2xl mx-4">
            <div class="flex items-center bg-void rounded-lg px-4 py-2 border border-white/10 focus-within:border-matrix transition-colors">
                <span class="text-matrix font-mono font-bold mr-3 animate-pulse">></span>
                <input type="text" id="cli-input" class="w-full bg-transparent text-sm font-mono text-white focus:outline-none placeholder:text-muted" placeholder="Type '/' to focus. Ex: filter --lang rust --stars >100">
            </div>
        </div>

        <div class="flex items-center gap-4">
            <button class="text-muted hover:text-white transition-colors"><i data-lucide="bell"></i></button>
            <img src="https://avatars.githubusercontent.com/u/9919?v=4" alt="User" class="w-9 h-9 rounded-full border border-white/20">
        </div>
    </header>

    <main class="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- 2. The Identity Matrix (Left Sidebar) -->
        <aside class="lg:col-span-3 glass-panel rounded-xl p-6 flex flex-col gap-8 h-fit">
            <!-- Profile Info -->
            <div class="text-center">
                <div class="relative inline-block mb-4">
                    <img src="https://avatars.githubusercontent.com/u/9919?v=4" alt="Profile" class="w-24 h-24 rounded-2xl border border-white/10 shadow-[0_0_20px_rgba(255,255,255,0.05)] mx-auto">
                    <div class="absolute -bottom-2 -right-2 bg-purple text-white text-xs font-mono font-bold px-2 py-1 rounded-md shadow-[0_0_10px_rgba(176,38,255,0.5)]">LVL 42</div>
                </div>
                <h1 class="text-xl font-bold text-white">Alex Developer</h1>
                <p class="text-muted font-mono text-sm mt-1">@alex_dev</p>
            </div>

            <!-- EXP Bar -->
            <div>
                <div class="flex justify-between text-xs font-mono mb-2">
                    <span class="text-purple font-bold">EXP</span>
                    <span class="text-muted">8,450 / 10,000</span>
                </div>
                <progress value="8450" max="10000" class="w-full h-2 rounded-full"></progress>
            </div>

            <!-- Gamification Badges -->
            <div>
                <h3 class="text-sm font-mono text-muted uppercase tracking-widest mb-4 border-b border-white/10 pb-2">Unlocked Assets</h3>
                <div class="grid grid-cols-4 gap-3">
                    <!-- Polyglot Master -->
                    <div class="aspect-square glass-panel rounded-lg flex items-center justify-center neon-border-cyan cursor-crosshair group relative" title="Polyglot Master">
                        <i data-lucide="component" class="text-cyan group-hover:animate-pulse"></i>
                    </div>
                    <!-- Core Cartographer -->
                    <div class="aspect-square glass-panel rounded-lg flex items-center justify-center neon-border-purple cursor-crosshair group relative" title="Core Cartographer">
                        <i data-lucide="map" class="text-purple group-hover:animate-pulse"></i>
                    </div>
                    <!-- Green Supreme -->
                    <div class="aspect-square glass-panel rounded-lg flex items-center justify-center neon-border-cyan cursor-crosshair group relative" title="Green Supreme">
                        <i data-lucide="check-circle-2" class="text-matrix group-hover:animate-pulse"></i>
                    </div>
                    <!-- Critical Defusal -->
                    <div class="aspect-square glass-panel rounded-lg flex items-center justify-center neon-border-purple cursor-crosshair group relative" title="Critical Defusal">
                        <i data-lucide="timer" class="text-[#FF3366] group-hover:animate-pulse"></i>
                    </div>
                    <!-- Placeholder Badges -->
                    <div class="aspect-square bg-white/5 border border-white/5 rounded-lg flex items-center justify-center opacity-30"><i data-lucide="lock" class="w-4 h-4 text-muted"></i></div>
                    <div class="aspect-square bg-white/5 border border-white/5 rounded-lg flex items-center justify-center opacity-30"><i data-lucide="lock" class="w-4 h-4 text-muted"></i></div>
                    <div class="aspect-square bg-white/5 border border-white/5 rounded-lg flex items-center justify-center opacity-30"><i data-lucide="lock" class="w-4 h-4 text-muted"></i></div>
                    <div class="aspect-square bg-white/5 border border-white/5 rounded-lg flex items-center justify-center opacity-30"><i data-lucide="lock" class="w-4 h-4 text-muted"></i></div>
                </div>
            </div>
        </aside>

        <!-- 3. The Main Stage (Center Console) -->
        <section class="lg:col-span-9 flex flex-col gap-6">
            <h2 class="text-sm font-mono text-muted uppercase tracking-widest flex items-center gap-2">
                <i data-lucide="zap" class="w-4 h-4 text-cyan"></i> Priority Vectors (Pinned)
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Repo Card 1 -->
                <div class="glass-panel rounded-xl p-6 neon-border-cyan group flex flex-col h-64 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-cyan/10 blur-3xl rounded-full group-hover:bg-cyan/20 transition-colors"></div>
                    
                    <div class="flex justify-between items-start mb-4 z-10">
                        <h3 class="text-lg font-bold text-white group-hover:text-cyan transition-colors flex items-center gap-2">
                            <i data-lucide="book-marked" class="w-5 h-5"></i>
                            quantum-engine
                        </h3>
                        <span class="px-2 py-1 bg-white/5 border border-white/10 rounded-md text-xs font-mono text-muted flex items-center gap-1">
                            Public
                        </span>
                    </div>
                    
                    <p class="text-sm text-muted mb-auto z-10">High-performance Rust framework for distributed systems. Built for the modern web with an emphasis on memory safety.</p>
                    
                    <div class="flex items-center gap-4 mt-4 pt-4 border-t border-white/10 z-10 text-sm font-mono">
                        <div class="flex items-center gap-1.5 text-muted">
                            <div class="w-2.5 h-2.5 rounded-full bg-[#dea584]"></div> Rust
                        </div>
                        <div class="flex items-center gap-1.5 text-muted group-hover:text-white transition-colors cursor-pointer">
                            <i data-lucide="star" class="w-4 h-4"></i> <span class="odometer">1,420</span>
                        </div>
                        <div class="flex items-center gap-1.5 text-muted group-hover:text-white transition-colors cursor-pointer">
                            <i data-lucide="git-fork" class="w-4 h-4"></i> 245
                        </div>
                    </div>
                </div>

                <!-- Repo Card 2 -->
                <div class="glass-panel rounded-xl p-6 neon-border-purple group flex flex-col h-64 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-purple/10 blur-3xl rounded-full group-hover:bg-purple/20 transition-colors"></div>
                    
                    <div class="flex justify-between items-start mb-4 z-10">
                        <h3 class="text-lg font-bold text-white group-hover:text-purple transition-colors flex items-center gap-2">
                            <i data-lucide="book-marked" class="w-5 h-5"></i>
                            nexus-ui
                        </h3>
                        <span class="px-2 py-1 bg-white/5 border border-white/10 rounded-md text-xs font-mono text-muted flex items-center gap-1">
                            Public
                        </span>
                    </div>
                    
                    <p class="text-sm text-muted mb-auto z-10">Glassmorphic React component library powered by Tailwind CSS. Bring your dashboard to the year 2045.</p>
                    
                    <div class="flex items-center gap-4 mt-4 pt-4 border-t border-white/10 z-10 text-sm font-mono">
                        <div class="flex items-center gap-1.5 text-muted">
                            <div class="w-2.5 h-2.5 rounded-full bg-[#3178c6]"></div> TypeScript
                        </div>
                        <div class="flex items-center gap-1.5 text-muted group-hover:text-white transition-colors cursor-pointer">
                            <i data-lucide="star" class="w-4 h-4 text-purple"></i> <span class="odometer text-purple">4,092</span>
                        </div>
                        <div class="flex items-center gap-1.5 text-muted group-hover:text-white transition-colors cursor-pointer">
                            <i data-lucide="git-fork" class="w-4 h-4"></i> 891
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. The Activity Engine (Interactive Heatmap) -->
            <div class="glass-panel rounded-xl p-6 mt-2">
                <div class="flex justify-between items-end mb-6">
                    <h2 class="text-sm font-mono text-muted uppercase tracking-widest flex items-center gap-2">
                        <i data-lucide="activity" class="w-4 h-4 text-matrix"></i> Biometrics (Last 12 Months)
                    </h2>
                    <div class="text-xs font-mono text-muted flex gap-2 items-center">
                        Less <div class="flex gap-1">
                            <div class="w-3 h-3 rounded-sm bg-[#161B22]"></div>
                            <div class="w-3 h-3 rounded-sm bg-[#0E4429]"></div>
                            <div class="w-3 h-3 rounded-sm bg-[#006D32]"></div>
                            <div class="w-3 h-3 rounded-sm bg-[#26A641]"></div>
                            <div class="w-3 h-3 rounded-sm bg-[#39D353]"></div>
                        </div> More
                    </div>
                </div>
                
                <!-- JS Generated Heatmap Container -->
                <div class="overflow-x-auto pb-4">
                    <div id="heatmap-container" class="grid grid-rows-7 grid-flow-col gap-[3px] min-w-max">
                        <!-- Blocks generated by JS -->
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Initialize Lucide Icons
        lucide.createIcons();

        // 1. Interactive Heatmap Generation
        const heatmapContainer = document.getElementById('heatmap-container');
        const weeks = 52;
        const daysInWeek = 7;
        const totalDays = weeks * daysInWeek;
        
        // GitHub contribution colors
        const colors = ['#161B22', '#0E4429', '#006D32', '#26A641', '#39D353'];

        for (let i = 0; i < totalDays; i++) {
            const block = document.createElement('div');
            block.className = 'heatmap-block';
            
            // Randomize activity level (bias towards empty/low for realism)
            const rand = Math.random();
            let colorIndex = 0;
            if (rand > 0.6) colorIndex = 1;
            if (rand > 0.8) colorIndex = 2;
            if (rand > 0.9) colorIndex = 3;
            if (rand > 0.95) colorIndex = 4;

            block.style.backgroundColor = colors[colorIndex];
            
            // Tooltip simulation
            block.title = `${Math.floor(Math.random() * 15)} contributions on this day`;
            
            heatmapContainer.appendChild(block);
        }

        // 2. Simulated CLI Interaction
        const cliInput = document.getElementById('cli-input');
        const appBody = document.getElementById('app-body');

        // Press '/' to focus input
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== cliInput) {
                e.preventDefault();
                cliInput.focus();
            }
        });

        // Press 'Enter' to execute mock command
        cliInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && cliInput.value.trim() !== '') {
                // Apply a glitch/flicker effect to the UI
                appBody.classList.add('animate-flicker');
                
                // Clear input after a short delay
                setTimeout(() => {
                    cliInput.value = '';
                    appBody.classList.remove('animate-flicker');
                }, 300);
            }
        });

        // 3. Odometer mock hover effect
        const odometers = document.querySelectorAll('.odometer');
        odometers.forEach(odo => {
            odo.parentElement.addEventListener('mouseenter', () => {
                let currentVal = parseInt(odo.innerText.replace(/,/g, ''));
                odo.innerText = (currentVal + 1).toLocaleString();
            });
        });
    </script>
</body>
</html>
