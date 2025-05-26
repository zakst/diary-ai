import asyncio

from generation_utils import folder_selection, process_prompt


async def main():
  verbose_input = input("Verbose mode? (y/n) [n]: ").strip().lower()
  is_verbose = verbose_input == "y"
  selected_diary = await folder_selection()
  if selected_diary is None:
    return
  else:
    prompt = input(f"{selected_diary} > Enter your prompt: ")
    print("🤖 ...")
    response = await process_prompt(prompt, selected_diary, is_verbose)
    print("")
    print(response)

if __name__ == "__main__":
  asyncio.run(main())
