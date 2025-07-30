#!/usr/bin/env bash
set -e


major=0
minor=0
patch=1

help_str="
Usage: $0 [OPTIONS]

Options:
  -M, --major       Set major flag
  -m, --minor       Set minor flag
  -p, --patch       Set patch flag
  -h, --help        Show this help message and exit
"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -M|--major)
      major=1
      shift
      ;;
    -m|--minor)
      minor=1
      shift
      ;;
    -p|--patch)
      patch=1
      shift
      ;;
    -h|--help)
      echo "$help_str"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "$help_str"
      exit 1
      ;;
  esac
done

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Uncommitted changes found. Committing..."
  git add -A
  git commit -am "🔖 release commit"
  git push
fi

# Get last release commit
last_release_commit=$(git tag | grep '^release-' | sort -V | tail -n 1 | sed 's/^release-//')
if [ -z "$last_release_commit" ]; then
    echo "No previous release found. Making a new release."
    last_release_commit="0.0.0"
fi

IFS='.' read -r x y z <<< "$last_release_commit"

if [ "$major" -eq 1 ]; then
  x=$((x + 1))
  y=0
  z=0
elif [ "$minor" -eq 1 ]; then
  y=$((y + 1))
  z=0
elif [ "$patch" -eq 1 ]; then
  z=$((z + 1))
else
  echo "No version increment option provided. Exiting."
  exit 1
fi

tag_name="release-$x.$y.$z"

h1_title="# Release notes"
prv_notes=$(tail -n +2 notes/release-notes.md)

# Create a temp file for the user's message
tmpfile=$(mktemp)
echo "# Release notes for $tag_name
# Note h1(#) and h2(##) lines will be skipped
* 
" > "$tmpfile"

# Open vim for the user to write their message
vim +3 +'normal 2|' "$tmpfile"

# Read the contents into a variable
user_message=$(sed '/^##\? /d' $tmpfile)

# Optionally remove the temp file
rm "$tmpfile"

# Update the release notes file
echo -e "$h1_title\n\n## $tag_name $(date)\n\n$user_message\n$prv_notes" > notes/release-notes.md

# Commit the changes
git add notes/release-notes.md
git commit -m "📝 Update release notes for $tag_name"

# Tag the commit
tag_message="$tag_name
$user_message"
git tag -a "$tag_name" -m "$tag_message"
git push origin "$tag_name"
