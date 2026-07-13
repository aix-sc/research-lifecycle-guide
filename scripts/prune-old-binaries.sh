#!/usr/bin/env bash
#
# prune-old-binaries.sh — docs/ と templates/ のバイナリ成果物を「最新版のみ」に保つ
#
# 命名規則: {YYYYMMDD}_{名称}_v{X}_{LANG}.{pptx|docx|xlsx}
# 同じ「名称 × LANG × 拡張子」の系列について、バージョン番号 vX が最大のものだけを残し、
# それ以外（旧版）を git rm する。追跡外のローカル旧版も削除する。
#
# 使い方:
#   bash scripts/prune-old-binaries.sh            # 実行（削除まで行う）
#   bash scripts/prune-old-binaries.sh --dry-run  # 何を消すか表示するだけ
#
# 注: macOS 標準の bash 3.2 でも動くよう、連想配列を使わずに実装している。
#
set -eu
cd "$(dirname "$0")/.."

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN=1
fi

removed=0
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

for dir in docs templates; do
  [ -d "$dir" ] || continue

  # 「系列キー<TAB>バージョン<TAB>ファイルパス」の一覧を作る
  : > "$tmpfile"
  find "$dir" -maxdepth 1 -type f \( -name "*.pptx" -o -name "*.docx" -o -name "*.xlsx" \) | sort | while IFS= read -r f; do
    base=$(basename "$f")
    # _vX を含まないファイルは版管理対象外 → 触らない
    case "$base" in
      *_v[0-9]*) ;;
      *) continue ;;
    esac
    ver=$(echo "$base" | sed -E 's/.*_v([0-9]+).*/\1/')
    # 系列キー: 先頭の日付プレフィックスと _vX を除去した残り
    key=$(echo "$base" | sed -E 's/^[0-9]{8}_//; s/_v[0-9]+//')
    printf '%s\t%s\t%s\n' "$key" "$ver" "$f" >> "$tmpfile"
  done

  [ -s "$tmpfile" ] || continue

  # 系列キーごとに最大バージョンを求め、それ以外を削除
  cut -f1 "$tmpfile" | sort -u | while IFS= read -r key; do
    maxver=$(awk -F'\t' -v k="$key" '$1==k {if ($2+0 > m) m=$2+0} END {print m+0}' "$tmpfile")
    awk -F'\t' -v k="$key" '$1==k {print $2"\t"$3}' "$tmpfile" | while IFS="$(printf '\t')" read -r ver f; do
      if [ "$ver" -eq "$maxver" ]; then
        echo "  ✅ 最新: $f  (v$ver)"
      else
        echo "  🗑  旧版: $f  (v$ver < v$maxver)"
        if [ "$DRY_RUN" -eq 0 ]; then
          git rm --quiet --ignore-unmatch "$f" 2>/dev/null || rm -f "$f"
          echo "x" >> "$tmpfile.removed"
        fi
      fi
    done
  done
done

if [ -f "$tmpfile.removed" ]; then
  removed=$(wc -l < "$tmpfile.removed" | tr -d ' ')
  rm -f "$tmpfile.removed"
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "（dry-run: 削除は行っていません）"
else
  echo "旧版を ${removed} 件削除しました（最新版のみ追跡）。"
fi
