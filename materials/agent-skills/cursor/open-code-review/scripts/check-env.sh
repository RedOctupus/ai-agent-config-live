#!/usr/bin/env bash
# OCR environment gate. stdout = JSON only. Never prints API keys.
# Usage: bash scripts/check-env.sh
#        bash scripts/check-env.sh --test-llm
set -u
TEST_LLM=0
if [ "${1:-}" = "--test-llm" ]; then TEST_LLM=1; fi

json_escape() {
  printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null ||
    printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
}

port_open() {
  python3 - "$1" <<'PY' 2>/dev/null && return 0
import socket, sys
s = socket.socket()
s.settimeout(0.4)
try:
    s.connect(("127.0.0.1", int(sys.argv[1])))
    sys.exit(0)
except Exception:
    sys.exit(1)
finally:
    s.close()
PY
  return 1
}

git_ok=false
git_ver=""
git_path="$(command -v git || true)"
if [ -n "$git_path" ]; then
  git_raw="$(git --version 2>/dev/null || true)"
  git_ver="$(printf '%s' "$git_raw" | awk '{print $3}')"
  git_maj="${git_ver%%.*}"
  git_rest="${git_ver#*.}"
  git_min="${git_rest%%.*}"
  if [ "${git_maj:-0}" -gt 2 ] || { [ "${git_maj:-0}" -eq 2 ] && [ "${git_min:-0}" -ge 41 ]; }; then
    git_ok=true
  fi
fi

ocr_ok=false
ocr_ver=""
ocr_path="$(command -v ocr || true)"
ocr_raw=""
if [ -n "$ocr_path" ]; then
  ocr_ok=true
  ocr_raw="$(ocr version 2>/dev/null | head -n 1 || true)"
  ocr_ver="$(printf '%s' "$ocr_raw" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)"
fi

node_ok=false
node_ver=""
node_path="$(command -v node || true)"
if [ -n "$node_path" ]; then
  node_ver="$(node -v 2>/dev/null || true)"
  node_maj="$(printf '%s' "$node_ver" | tr -dc '0-9\n' | head -c 2)"
  node_maj="${node_ver#v}"
  node_maj="${node_maj%%.*}"
  if [ "${node_maj:-0}" -ge 18 ]; then node_ok=true; fi
fi

cfg="$HOME/.opencodereview/config.json"
llm_configured=false
llm_provider=""
llm_model=""
llm_language=""
env_hints=""

hint() {
  eval "val=\${$2-}"
  if [ -n "${val:-}" ]; then
    if [ -n "$env_hints" ]; then env_hints="$env_hints,\"$1\""; else env_hints="\"$1\""; fi
  fi
}
hint deepseek DEEPSEEK_API_KEY
hint dashscope DASHSCOPE_API_KEY
hint kimi MOONSHOT_API_KEY
hint openai OPENAI_API_KEY
hint anthropic ANTHROPIC_API_KEY
hint volcengine ARK_API_KEY

if [ -f "$cfg" ] && command -v python3 >/dev/null; then
  eval "$(python3 - "$cfg" <<'PY'
import json, sys, os
p = sys.argv[1]
try:
    c = json.load(open(p, encoding="utf-8"))
except Exception:
    sys.exit(0)
provider = c.get("provider") or ""
language = c.get("language") or ""
model = c.get("model") or ""
configured = False
prov = (c.get("providers") or {}).get(provider) or {}
cust = (c.get("custom_providers") or {}).get(provider) or {}
block = prov or cust
if block.get("model"):
    model = block.get("model")
if block.get("api_key") or block.get("api_key_cmd") or block.get("url"):
    configured = True
llm = c.get("llm") or {}
if llm.get("auth_token") or llm.get("url"):
    configured = True
print("llm_provider=" + json.dumps(provider))
print("llm_model=" + json.dumps(model or ""))
print("llm_language=" + json.dumps(language or ""))
print("llm_configured=" + ("true" if configured else "false"))
PY
)"
fi

if [ "$llm_configured" != "true" ] && [ -n "$env_hints" ]; then
  llm_configured=true
fi

llm_tested="null"
if [ "$TEST_LLM" -eq 1 ] && [ "$ocr_ok" = true ]; then
  if ocr llm test 2>&1 | grep -Eqi 'successful|成功'; then
    llm_tested=true
  else
    llm_tested=false
  fi
fi

viewer_running=false
if port_open 5483; then viewer_running=true; fi

install="npm"
install_reason="npm wrapper auto-updates; needs Node.js 18+"
if [ "$node_ok" = true ]; then
  install="npm"
  install_reason="detected $node_ver, recommend npm"
else
  uname_s="$(uname -s 2>/dev/null || echo unknown)"
  case "$uname_s" in
    Darwin) install="homebrew"; install_reason="no Node.js 18+; recommend brew install open-code-review" ;;
    Linux) install="install-sh"; install_reason="no Node.js 18+; recommend install.sh" ;;
  esac
fi

provider_rec="deepseek"
provider_reason="no API key env var detected; DeepSeek is a common default"
if [ -n "$env_hints" ]; then
  provider_rec="$(printf '%s' "$env_hints" | sed 's/^"//;s/".*//')"
  provider_reason="detected matching provider env var"
elif [ -n "$llm_provider" ]; then
  provider_rec="$llm_provider"
  provider_reason="config.json provider=$llm_provider"
fi

missing=""
[ "$git_ok" = true ] || missing='"git>=2.41"'
if [ "$ocr_ok" != true ]; then
  if [ -n "$missing" ]; then missing="$missing,\"ocr\""; else missing='"ocr"'; fi
fi

ready=""
if [ "$ocr_ok" = true ] && [ "$git_ok" = true ]; then
  ready='"delegate"'
  if [ "$llm_configured" = true ]; then
    ready='"delegate","review","scan"'
  fi
fi

ok=false
next="start-viewer"
if [ "$git_ok" = true ] && [ "$ocr_ok" = true ]; then ok=true; fi
if [ "$git_ok" != true ]; then next="init-git"
elif [ "$ocr_ok" != true ]; then next="init-install"
elif [ "$llm_configured" != true ]; then next="init-llm"
elif [ "$llm_tested" = "false" ]; then next="init-llm"
elif [ "$viewer_running" = true ]; then next="dispatch"
fi

cat <<EOF
{
  "ok": $ok,
  "next": "$next",
  "missing": [${missing}],
  "ready_for": [${ready}],
  "git": {"ok": $git_ok, "version": $(json_escape "$git_ver"), "path": $(json_escape "$git_path")},
  "ocr": {"ok": $ocr_ok, "version": $(json_escape "$ocr_ver"), "path": $(json_escape "$ocr_path")},
  "node": {"ok": $node_ok, "version": $(json_escape "$node_ver")},
  "llm": {"configured": $llm_configured, "tested": $llm_tested, "provider": $(json_escape "$llm_provider"), "model": $(json_escape "$llm_model"), "language": $(json_escape "$llm_language"), "env_hints": [${env_hints}]},
  "viewer": {"running": $viewer_running, "url": "http://localhost:5483", "addr": "localhost:5483"},
  "recommend": {"install": "$install", "install_reason": $(json_escape "$install_reason"), "provider": "$provider_rec", "provider_reason": $(json_escape "$provider_reason")}
}
EOF

exit 0
