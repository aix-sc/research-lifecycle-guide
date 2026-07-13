#!/usr/bin/env bash
#
# prune-old-binaries.sh — docs/ と templates/ のバイナリ成果物を「最新版のみ」に保つ
#
# 命名規則: {YYYYMMDD}_{名称}_v{X}_{LANG}.{pptx|docx}
# 同じ「名称 × LANG × 拡張子」の系列について、バージョン番号 vX が最大のものだけを残し、
# それ以外（旧版）を git rm する。追跡外のローカル旧版も削除する。
#
# 使い方:
#   bash scripts/prune-old-binaries.sh          # 実行（削除まで行う）
#   bash scripts/prune-old-binaries.sh --dry-run  # 何を消すか表示するだけ
#
set -euo pipefail
cd "$(dirname "$0")/.."

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

removed=0

for dir in docs templates; do
  [[ -d "$dir" ]] || continue

  # 対象ファイルを列挙し、「系列キー」でグルーピングする
  # 系列キー = 日付とバージョンを除いた部分（名称＋LANG＋拡張子）
  declare -A best_ver=()
  declare -A best_file=()

  while IFS= read -r f; do
    base=$(basename "$f")
    # vX を抽出（無ければスキップ＝版管理対象外のファイルは触らない）
    if [[ ! "$base" =~ _v([0-9]+) ]]; then
      continue
    fi
    ver="${BASH_REMATCH[1]}"
    # 系列キー：日付プレフィックスと _vX を取り除いた残り
    key=$(echo "$base" | sed -E 's/^[0-9]{8}_//; s/_v[0-9]+//')
    key="$dir/$key"

    if [[ -z "${best_ver[$key]:-}" ]] || (( ver > best_ver[$key] )); then
      # これまでの最良版があれば、それは旧版になる
      if [[ -n "${best_file[$key]:-}" ]]; then
        echo "  旧版: ${best_file[$key]}  (v${best_ver[$key]} < v${ver})"
        if (( DRY_RUN == 0 )); then
          git rm --quiet --ignore-unmatch "${best_file[$key]}" 2>/dev/null || rm -f "${best_file[$key]}"
          removed=$((removed+1))
        fi
      fi
      best_ver[$key]=$ver
      best_file[$key]="$f"
    else
      echo "  旧版: $f  (v${ver} < v${best_ver[$key]})"
      if (( DRY_RUN == 0 )); then
        git rm --quiet --ignore-unmatch "$f" 2>/dev/null || rm -f "$f"
        removed=$((removed+1))
      fi
    fi
  done < <(find "$dir" -maxdepth 1 -type f \( -name "*.pptx" -o -name "*.docx" -o -name "*.xlsx" \) | sort)

  # 残った最新版を報告
  for key in "${!best_file[@]}"; do
    echo "  ✅ 最新: ${best_file[$key]}  (v${best_ver[$key]})"
  done

  unset best_ver best_file
done

if (( DRY_RUN == 1 )); then
  echo "（dry-run: 削除は行っていません）"
else
  echo "旧版を ${removed} 件削除しました（最新版のみ追跡）。"
fi
