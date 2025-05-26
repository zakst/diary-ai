from pathlib import Path
from typing import Optional


async def folder_selection() -> Optional[str]:
  diary_path = Path("diary_samples")
  if not diary_path.exists() or not diary_path.is_dir():
    print("❌ 'diary_samples' directory not found.")
    return None

  folders = [f.name for f in diary_path.iterdir() if f.is_dir()]
  if not folders:
    print("❌ No folders found in 'diary_samples'.")
    return None

  print("\nAvailable users:")
  for i, folder in enumerate(folders, 1):
    print(f"{folder}")

  while True:
    choice = input("\nLog in as: ").strip()
    if choice in folders:
      break
    else:
      print("❌ Invalid choice. Please try again.")
  return choice
