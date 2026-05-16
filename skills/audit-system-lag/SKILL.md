---
name: audit-system-lag
description: Audit system resources - find memory hogs, zombie processes, and fix lag. Use when the system is slow or unresponsive.
allowed-tools: Bash
---

# System Audit Skill

Quick diagnostics for when the system is laggy. Run these checks in order.

## 1. Quick System Status

```bash
top -l 1 | head -8
```

**What to look for:**
- Load Avg > core count = overloaded
- CPU idle < 20% = maxed out
- PhysMem "unused" < 1GB = memory pressure
- Compressor > 10GB = heavy swapping

## 2. Top Memory Hogs

```bash
ps aux -m | head -20
```

## 3. Find Zombie Node/Claude Processes

Long-running Node processes (dev servers, Claude sessions) leak memory over time.

```bash
# Find all node/claude processes with runtime and memory
ps aux | grep -E "node|claude" | grep -v grep | awk '{
  cmd = $11; for(i=12;i<=NF;i++) cmd = cmd " " $i
  printf "%s %s %s %s\n", $2, $4"%", $10, substr(cmd, 1, 60)
}' | sort -k2 -rn | head -20
```

```bash
# Check what directories Claude sessions are in
for pid in $(pgrep -x claude); do
  cwd=$(lsof -p $pid 2>/dev/null | grep cwd | awk '{print $9}')
  etime=$(ps -p $pid -o etime= 2>/dev/null | tr -d ' ')
  mem=$(ps -p $pid -o rss= 2>/dev/null | awk '{printf "%.1fGB", $1/1024/1024}')
  echo "$etime | $mem | $pid | $cwd"
done | sort -t'|' -k1 -r
```

## 4. Find Stale Next.js Dev Servers

```bash
ps aux | grep -E "next-server|next-router" | grep -v grep | awk '{print $2, $10, $11, $12, $13}'
```

## 5. Kill Actions

**Kill all Claude sessions except one (replace KEEP_PID):**
```bash
pgrep -x claude | grep -v "^KEEP_PID$" | xargs kill -9
```

**Kill specific PIDs:**
```bash
kill -9 PID1 PID2 PID3
```

**Kill all Next.js dev servers:**
```bash
pkill -9 -f "next-server"
```

## 6. Verify Cleanup

```bash
echo "Claude: $(pgrep -x claude | wc -l) | Node: $(pgrep node | wc -l)"
top -l 1 | grep -E "Load Avg|PhysMem|CPU usage"
```

## Common Culprits

1. **Claude Code sessions** - leak ~500MB/day, kill after 24h+ runtime
2. **Next.js dev servers** - leak heavily, kill if running 1d+
3. **Cursor Helper (Renderer)** - each window uses 1-3GB, close unused windows
4. **Figma** - GPU helper uses 3-5GB, close when not designing

## Quick Fix Sequence

1. Kill zombie Claude sessions (keep current one)
2. Kill old Next.js dev servers
3. Close unused Cursor windows
4. Close Figma if not using
5. If still bad, restart machine
