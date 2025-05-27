import asyncio
import os

from generation_utils import folder_selection, process_prompt
GENERATION_API = os.getenv("GENERATION_API")

async def main():
  verbose_input = input("Verbose mode? (y/n) [n]: ").strip().lower()
  is_verbose = verbose_input == "y"
  selected_diary = await folder_selection()
  if selected_diary is None:
    return
  else:
    prompt = input(f"{selected_diary} > Enter your prompt: ")
    print(f"🤖 {GENERATION_API}...")
    response = await process_prompt(prompt, selected_diary, is_verbose)
    if response is None:
      print("❌ GENERATION_API in .env can be either openai or gemini")
    else:
      print("")
      print(response)

if __name__ == "__main__":
  asyncio.run(main())
