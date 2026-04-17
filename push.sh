#!/bin/bash
# push.sh — remote별 push 처리
#
# origin (개인깃):    team/ 제외 (gitignore 그대로)
# core-shell (팀깃):  team/ 포함 (임시 브랜치로 처리)
#
# 사용법:
#   ./push.sh            → origin + core-shell 둘 다
#   ./push.sh origin     → 개인깃만
#   ./push.sh team       → 팀깃만 (team/ 포함)

set -e

REMOTE=${1:-"all"}
CURRENT=$(git branch --show-current)

push_origin() {
  echo "→ origin push (team/ 제외)"
  git push origin main
  echo "✓ origin 완료"
}

push_team() {
  echo "→ core-shell push (team/ 포함)"

  # 임시 브랜치
  git checkout -b _team_push_temp 2>/dev/null

  # team/ 강제 스테이징
  # team/ 디렉토리가 .gitignore에 통째로 있으면 git add -f team/ 가 재귀 안 함
  # → find로 개별 파일을 직접 추가 (node_modules/.next 등 대용량 제외)
  find team/ -type f \
    ! -path "*/node_modules/*" \
    ! -path "*/.next/*" \
    ! -path "*/.yarn/cache/*" \
    -print0 | xargs -0 git add -f 2>/dev/null || true

  # 변경사항 있으면 커밋
  git diff --cached --quiet || git commit -m "chore: team/ 포함 (core-shell 전용 임시)"

  # push
  git push core-shell _team_push_temp:main --force

  # 정리
  git checkout "$CURRENT"
  git branch -D _team_push_temp

  echo "✓ core-shell 완료"
}

case "$REMOTE" in
  origin)
    push_origin
    ;;
  core-shell|team)
    push_team
    ;;
  all)
    push_origin
    push_team
    ;;
  *)
    echo "사용법: ./push.sh [origin|core-shell|team|all]"
    exit 1
    ;;
esac
