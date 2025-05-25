import asyncio

from generation_utils import folder_selection

async def main():
  selected_diary = await folder_selection()
  if selected_diary is None:
    return
  else:
    prompt


if __name__ == "__main__":
  asyncio.run(main())
