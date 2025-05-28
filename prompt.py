import asyncio
import os

from generation_utils import folder_selection, process_prompt
GENERATION_LLM = os.getenv("GENERATION_LLM")
IS_VERBOSE = os.getenv("VERBOSE")

async def main():
  is_verbose = IS_VERBOSE == "true"
  selected_diary = await folder_selection()
  if selected_diary is None:
    return
  else:
    prompt = input(f"{selected_diary} > Enter your prompt: ")
    print(f"🤖 {GENERATION_LLM}...")
    response = await process_prompt(prompt, selected_diary, is_verbose)
    if response is None:
      print("❌ GENERATION_LLM in .env can be either openai or gemini")
    else:
      print("")
      print(response)

if __name__ == "__main__":
  asyncio.run(main())
